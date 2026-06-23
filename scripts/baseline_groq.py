#!/usr/bin/env python3
"""Run the zero-shot Groq baseline LOCALLY (API call, no GPU).

This lets you test your SYSTEM_PROMPT and the output parsing before Colab. It
replicates the notebook's seeded, stratified 70/15/15 split (random_state=42) and
evaluates ONLY on the test split — so the local baseline equals what Colab would
produce, and you can skip re-running the baseline in Colab.

Usage:
    python scripts/baseline_groq.py data/dataset.csv
    python scripts/baseline_groq.py data/dataset.csv --limit 25   # quick smoke test

Requires GROQ_API_KEY in .env (see .env.example).
"""

import argparse
import os
import sys
import time

import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Reuse the project's label taxonomy so labels stay consistent everywhere.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_dataset import LABEL_MAP  # noqa: E402

MODEL = "llama-3.3-70b-versatile"

# Inference settings — kept identical to the notebook so local == Colab.
TEMPERATURE = 0
MAX_TOKENS = 20
REQUEST_DELAY_S = 0.1  # notebook sleeps 0.1s between requests (free-tier limits)

# Split settings — kept IDENTICAL to the notebook so the test split matches.
RANDOM_STATE = 42

# ---------------------------------------------------------------------------
# TODO (student): write the system prompt that instructs the model how to
# classify discourse quality. This is YOUR work — describe the task and your
# labels, and tell the model to respond with EXACTLY one label string from your
# taxonomy (the parser below does a substring match, longest-label-first).
#
# Tip: the model's reply should contain one of your label strings verbatim.
SYSTEM_PROMPT = """TODO: write your classification system prompt here."""
# ---------------------------------------------------------------------------


def make_splits(df: pd.DataFrame):
    """Replicate the notebook's seeded, stratified 70/15/15 split EXACTLY.

    The notebook (cell 8) does, in this order:
        train_df, temp_df = train_test_split(
            df, test_size=0.30, random_state=42, stratify=df["label_id"])
        val_df, test_df = train_test_split(
            temp_df, test_size=0.50, random_state=42, stratify=temp_df["label_id"])
        # then each split is reset_index(drop=True)

    Reproducing the exact call order and arguments is what makes the local
    test split identical to Colab's. Returns (train_df, val_df, test_df).
    Only test_df is scored here.
    """
    strat = df["label_id"]

    train_df, temp_df = train_test_split(
        df, test_size=0.30, random_state=RANDOM_STATE, stratify=strat
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, random_state=RANDOM_STATE, stratify=temp_df["label_id"]
    )

    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    return train_df, val_df, test_df


def parse_prediction(raw: str, labels: list[str]) -> str | None:
    """Parse the model's reply into one label.

    Matches the notebook's parsing (cell 21): lowercase+strip the reply, then
    check longest labels first so a label that is a substring of another (e.g.
    "recommendation" vs. "strong_recommendation") can't be matched by mistake.
    A label matches if it equals the reply OR appears as a substring of it.
    Returns None if no label is found (counts as unparseable).
    """
    text = (raw or "").strip().lower()
    for lbl in sorted(labels, key=len, reverse=True):
        low = lbl.lower()
        if text == low or low in text:
            return lbl
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="data/dataset.csv",
        help="Path to the dataset CSV (default: data/dataset.csv)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only classify the first N test rows (smoke test / save API calls).",
    )
    args = parser.parse_args()

    # --- Preconditions ----------------------------------------------------
    if not LABEL_MAP:
        print(
            "❌ LABEL_MAP is empty — fill it in scripts/validate_dataset.py first.",
            file=sys.stderr,
        )
        return 1
    if "TODO" in SYSTEM_PROMPT:
        print(
            "❌ SYSTEM_PROMPT still contains the TODO placeholder — write your "
            "prompt at the top of this script before running.",
            file=sys.stderr,
        )
        return 1

    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print(
            "❌ GROQ_API_KEY not set. Copy .env.example to .env and add your key.",
            file=sys.stderr,
        )
        return 1

    try:
        from groq import Groq
    except ImportError:
        print(
            "❌ groq not installed. Run: pip install -r requirements-local.txt",
            file=sys.stderr,
        )
        return 1

    # --- Load + split -----------------------------------------------------
    # Mirror the notebook: map labels -> label_id, drop rows whose label isn't
    # in LABEL_MAP, and stratify the split on label_id.
    df = pd.read_csv(args.csv_path)
    df = df.dropna(subset=["text", "label"]).reset_index(drop=True)
    labels = list(LABEL_MAP.keys())

    df["label_id"] = df["label"].map(LABEL_MAP)
    dropped = int(df["label_id"].isna().sum())
    if dropped:
        print(
            f"⚠️  dropping {dropped} row(s) whose label isn't in LABEL_MAP "
            "(run scripts/validate_dataset.py to see which).",
            file=sys.stderr,
        )
    df = df.dropna(subset=["label_id"]).reset_index(drop=True)
    df["label_id"] = df["label_id"].astype(int)

    _, _, test_df = make_splits(df)
    if args.limit is not None:
        test_df = test_df.head(args.limit)
    print(f"Scoring {len(test_df)} test rows with {MODEL} (zero-shot)...\n")

    client = Groq(api_key=api_key)

    y_true: list[str] = []
    y_pred: list[str] = []
    unparseable = 0

    for i, (_, row) in enumerate(test_df.iterrows(), start=1):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    # Match the notebook's user-message format exactly.
                    {"role": "user", "content": f"Classify this post:\n\n{row['text']}"},
                ],
            )
            raw = resp.choices[0].message.content
        except Exception as exc:  # noqa: BLE001 - keep going on transient errors
            print(f"  row {i}: API error: {exc}", file=sys.stderr)
            raw = ""

        pred = parse_prediction(raw, labels)
        if pred is None:
            unparseable += 1
            print(f"  row {i}: UNPARSEABLE -> {raw!r}")
            # Excluded from metrics; tracked separately as unparseable count.
        else:
            y_true.append(str(row["label"]).strip())
            y_pred.append(pred)
        if i % 10 == 0:
            print(f"  ...{i}/{len(test_df)} done")
        time.sleep(REQUEST_DELAY_S)  # notebook respects free-tier rate limits

    # --- Report -----------------------------------------------------------
    print("\n" + "=" * 60)
    print("Groq zero-shot baseline — test split")
    print("=" * 60)
    print(f"Test rows:        {len(test_df)}")
    print(f"Unparseable:      {unparseable}")
    print(f"Scored (parsed):  {len(y_pred)}")

    if y_pred:
        acc = accuracy_score(y_true, y_pred)
        print(f"\nAccuracy (parsed only): {acc:.4f}")
        print("\nPer-class report:")
        print(
            classification_report(
                y_true,
                y_pred,
                labels=labels,
                zero_division=0,
            )
        )
    else:
        print("\nNo parseable predictions — check SYSTEM_PROMPT / parsing.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
