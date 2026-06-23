#!/usr/bin/env python3
"""Validate the TakeMeter dataset BEFORE uploading it to Colab (no GPU needed).

Checks structure, label coverage, class balance, and common data-quality issues
so you don't waste a Colab run on a broken CSV.

Usage:
    python scripts/validate_dataset.py data/dataset.csv

Exit code is nonzero on a HARD FAILURE (missing columns, unmapped labels, null/
empty text). Warnings (balance, size, duplicates, short posts) do not fail the
run on their own but you should read them.
"""

import argparse
import sys

import pandas as pd

# ---------------------------------------------------------------------------
# TODO (student): define your label taxonomy here.
# Keys = the EXACT label strings that appear in the CSV's `label` column.
# Values = the integer class id used by the model (0..N-1, contiguous).
# This MUST match the labels in planning.md, the README, and the Colab notebook.
#
# Example shape only (replace with YOUR labels — do not ship these):
#   LABEL_MAP = {
#       "your_label_a": 0,
#       "your_label_b": 1,
#       "your_label_c": 2,
#   }
LABEL_MAP = {}  # TODO: fill in
# ---------------------------------------------------------------------------

# Tunable thresholds for warnings.
MAX_CLASS_FRACTION = 0.70   # warn if any class is >70% of the data
MIN_CLASS_FRACTION = 0.20   # warn if any class is <20% of the data
MIN_TOTAL_ROWS = 200        # warn if fewer than 200 rows total
SHORT_TEXT_CHARS = 10       # flag posts with fewer than this many characters

REQUIRED_COLUMNS = ["text", "label"]


def _fail(msg: str, hard_failures: list) -> None:
    print(f"  ❌ FAIL: {msg}")
    hard_failures.append(msg)


def _warn(msg: str, warnings: list) -> None:
    print(f"  ⚠️  WARN: {msg}")
    warnings.append(msg)


def _ok(msg: str) -> None:
    print(f"  ✅ {msg}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="data/dataset.csv",
        help="Path to the dataset CSV (default: data/dataset.csv)",
    )
    args = parser.parse_args()

    hard_failures: list[str] = []
    warnings: list[str] = []

    print(f"Validating: {args.csv_path}\n")

    # --- Load -------------------------------------------------------------
    try:
        df = pd.read_csv(args.csv_path)
    except FileNotFoundError:
        print(f"❌ FAIL: file not found: {args.csv_path}")
        return 1
    except Exception as exc:  # noqa: BLE001 - surface any parse error clearly
        print(f"❌ FAIL: could not read CSV: {exc}")
        return 1

    # --- LABEL_MAP sanity -------------------------------------------------
    print("LABEL_MAP")
    if not LABEL_MAP:
        _fail(
            "LABEL_MAP is empty — edit the TODO at the top of this script "
            "with your label taxonomy.",
            hard_failures,
        )
    else:
        _ok(f"{len(LABEL_MAP)} labels defined: {sorted(LABEL_MAP)}")
        ids = sorted(LABEL_MAP.values())
        if ids != list(range(len(ids))):
            _warn(
                f"class ids are not contiguous 0..N-1: {ids}",
                warnings,
            )

    # --- Columns ----------------------------------------------------------
    print("\nColumns")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        _fail(f"missing required column(s): {missing}", hard_failures)
        # Without text/label we can't do the rest meaningfully.
        return _summary(hard_failures, warnings)
    _ok(f"found required columns: {REQUIRED_COLUMNS}")
    if "notes" not in df.columns:
        _warn("no `notes` column (optional, but the template includes it)", warnings)

    print(f"\nTotal rows: {len(df)}")
    if len(df) < MIN_TOTAL_ROWS:
        _warn(
            f"only {len(df)} rows (<{MIN_TOTAL_ROWS}); consider collecting more.",
            warnings,
        )

    # --- Text quality -----------------------------------------------------
    print("\nText quality")
    text = df["text"]

    null_text = text.isna()
    empty_text = text.fillna("").astype(str).str.strip() == ""
    bad_text = null_text | empty_text
    if bad_text.any():
        rows = (df.index[bad_text] + 2).tolist()  # +2: header + 1-based
        _fail(
            f"{int(bad_text.sum())} row(s) have null/empty text "
            f"(CSV lines {rows[:10]}{'...' if len(rows) > 10 else ''})",
            hard_failures,
        )
    else:
        _ok("no null/empty text")

    # Duplicates (exact match on stripped text), ignoring already-bad rows.
    norm = text.fillna("").astype(str).str.strip()
    dup_mask = norm.duplicated(keep="first") & ~bad_text
    if dup_mask.any():
        rows = (df.index[dup_mask] + 2).tolist()
        _warn(
            f"{int(dup_mask.sum())} exact-duplicate text row(s) "
            f"(CSV lines {rows[:10]}{'...' if len(rows) > 10 else ''})",
            warnings,
        )
    else:
        _ok("no exact-duplicate text")

    # Very short posts.
    short_mask = (norm.str.len() < SHORT_TEXT_CHARS) & ~bad_text
    if short_mask.any():
        rows = (df.index[short_mask] + 2).tolist()
        _warn(
            f"{int(short_mask.sum())} very short post(s) (<{SHORT_TEXT_CHARS} "
            f"chars) (CSV lines {rows[:10]}{'...' if len(rows) > 10 else ''})",
            warnings,
        )
    else:
        _ok(f"no posts shorter than {SHORT_TEXT_CHARS} chars")

    # --- Label coverage ---------------------------------------------------
    print("\nLabel coverage")
    label = df["label"].fillna("").astype(str).str.strip()
    null_label = df["label"].isna() | (label == "")
    if null_label.any():
        rows = (df.index[null_label] + 2).tolist()
        _fail(
            f"{int(null_label.sum())} row(s) have null/empty label "
            f"(CSV lines {rows[:10]}{'...' if len(rows) > 10 else ''})",
            hard_failures,
        )

    if LABEL_MAP:
        unmapped = sorted(set(label[~null_label]) - set(LABEL_MAP))
        if unmapped:
            _fail(
                f"label(s) in CSV not present in LABEL_MAP: {unmapped}",
                hard_failures,
            )
        else:
            _ok("every label maps to LABEL_MAP")

        unused = sorted(set(LABEL_MAP) - set(label[~null_label]))
        if unused:
            _warn(f"LABEL_MAP labels with no rows: {unused}", warnings)

    # --- Distribution -----------------------------------------------------
    print("\nLabel distribution")
    counts = label[~null_label].value_counts()
    total = int(counts.sum())
    if total == 0:
        _fail("no valid labeled rows to summarize.", hard_failures)
    else:
        width = max((len(str(l)) for l in counts.index), default=5)
        for lbl, n in counts.sort_values(ascending=False).items():
            frac = n / total
            print(f"  {str(lbl):<{width}}  {n:>5}  ({frac:6.1%})")
        print(f"  {'TOTAL':<{width}}  {total:>5}")

        for lbl, n in counts.items():
            frac = n / total
            if frac > MAX_CLASS_FRACTION:
                _warn(
                    f"class '{lbl}' is {frac:.1%} (>{MAX_CLASS_FRACTION:.0%}); "
                    "data is imbalanced.",
                    warnings,
                )
            if frac < MIN_CLASS_FRACTION:
                _warn(
                    f"class '{lbl}' is {frac:.1%} (<{MIN_CLASS_FRACTION:.0%}); "
                    "may be under-represented.",
                    warnings,
                )

    return _summary(hard_failures, warnings)


def _summary(hard_failures: list, warnings: list) -> int:
    print("\n" + "=" * 60)
    print(f"Summary: {len(hard_failures)} hard failure(s), {len(warnings)} warning(s)")
    if hard_failures:
        print("\nHard failures (must fix before Colab):")
        for m in hard_failures:
            print(f"  - {m}")
        print("\nResult: NOT READY ❌")
        return 1
    if warnings:
        print("\nResult: usable, but review the warnings above ⚠️")
    else:
        print("\nResult: looks good ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
