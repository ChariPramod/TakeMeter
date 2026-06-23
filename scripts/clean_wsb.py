#!/usr/bin/env python3
"""Clean + sample the downloaded public r/wallstreetbets dataset (no GPU).

Turns the raw Kaggle-style dump (data/reddit_wsb.csv) into an annotation-ready
data/dataset.csv where:
  - `text` = title + " " + body   (per planning.md §2)
  - `label` is LEFT BLANK for you to annotate (one of the 4 labels, planning §3)
  - original metadata (id, score, comms_num, timestamp, url) is carried along

This script ONLY cleans, filters, dedups, and samples REAL rows from the file.
It does NOT assign labels and does NOT invent text — annotation is your work.

Cleaning steps:
  - build text = title + body (missing body -> empty string, per planning §2)
  - strip rows that are [removed]/[deleted]/empty or shorter than --min-chars
  - drop exact-duplicate text
  - random sample (seeded) down to --sample rows

Usage:
    python scripts/clean_wsb.py --in data/reddit_wsb.csv --out data/dataset.csv --sample 300

    # Bias the sample toward candidates for a hard-to-find class (planning §6):
    # this only SURFACES candidates by keyword; it does NOT label them.
    python scripts/clean_wsb.py --in data/reddit_wsb.csv --out data/candidates_dd.csv \
        --keywords "DD,calls,puts,position,short interest,catalyst" --sample 80

Then annotate the `label` column and run:
    python scripts/validate_dataset.py data/dataset.csv
"""

import argparse
import sys

import pandas as pd

# Columns kept from the raw dump (per planning.md §2 / §10). Order here is the
# output column order; `label` is inserted right after `text`.
RAW_TEXT_COLS = ["title", "body"]
META_COLS = ["id", "score", "comms_num", "timestamp", "url"]

REMOVED_MARKERS = {"[removed]", "[deleted]"}
RANDOM_STATE = 42  # seeded so the sample is reproducible


def build_text(df: pd.DataFrame) -> pd.Series:
    """text = title + ' ' + body, missing -> empty string, whitespace collapsed."""
    title = df["title"].fillna("").astype(str)
    body = df["body"].fillna("").astype(str)
    combined = (title + " " + body).str.replace(r"\s+", " ", regex=True).str.strip()
    return combined


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="in_path", default="data/reddit_wsb.csv",
                        help="raw WSB dataset CSV (default: data/reddit_wsb.csv)")
    parser.add_argument("--out", default="data/dataset.csv",
                        help="cleaned output CSV (default: data/dataset.csv)")
    parser.add_argument("--sample", type=int, default=300,
                        help="number of rows to keep (random, seeded). 0 = keep all.")
    parser.add_argument("--min-chars", type=int, default=20,
                        help="drop rows whose text is shorter than this (default 20)")
    parser.add_argument("--keywords", default="",
                        help="comma-separated terms; if set, keep only rows whose "
                             "text contains one (case-insensitive). Surfaces "
                             "candidates only — does NOT assign labels.")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.in_path)
    except FileNotFoundError:
        print(f"❌ raw dataset not found: {args.in_path}", file=sys.stderr)
        return 1

    missing = [c for c in RAW_TEXT_COLS if c not in df.columns]
    if missing:
        print(f"❌ raw dataset missing expected column(s): {missing}\n"
              f"   found: {list(df.columns)}", file=sys.stderr)
        return 1

    n_start = len(df)
    df["text"] = build_text(df)

    # Drop removed/deleted/empty and too-short.
    removed = df["text"].isin(REMOVED_MARKERS) | (df["text"].str.len() == 0)
    df = df[~removed]
    short = df["text"].str.len() < args.min_chars
    df = df[~short]

    # Drop exact-duplicate text (keep first).
    n_before_dedup = len(df)
    df = df.drop_duplicates(subset="text", keep="first")
    n_dups = n_before_dedup - len(df)

    # Optional keyword candidate filter (surfaces candidates; no labeling).
    if args.keywords.strip():
        terms = [t.strip().lower() for t in args.keywords.split(",") if t.strip()]
        pattern = "|".join(pd.Series(terms).str.replace(r"([.^$*+?()\[\]{}|\\])", r"\\\1", regex=True))
        mask = df["text"].str.lower().str.contains(pattern, regex=True, na=False)
        df = df[mask]
        print(f"keyword filter [{', '.join(terms)}]: {len(df)} candidate row(s)")

    n_usable = len(df)
    if n_usable == 0:
        print("❌ no usable rows after cleaning/filtering.", file=sys.stderr)
        return 1

    # Sample (seeded) if requested and we have more than enough.
    if args.sample and args.sample < n_usable:
        df = df.sample(n=args.sample, random_state=RANDOM_STATE)

    # Assemble output: text, blank label, then available metadata.
    df["label"] = ""  # BLANK on purpose — you annotate this.
    out_cols = ["text", "label"] + [c for c in META_COLS if c in df.columns]
    out = df[out_cols].reset_index(drop=True)

    out.to_csv(args.out, index=False)

    print(f"\n✅ Wrote {len(out)} rows to {args.out}")
    print(f"   raw rows: {n_start} | usable after cleaning: {n_usable} "
          f"(dropped {n_dups} duplicate, plus removed/short)")
    print("   The `label` column is BLANK — annotate each row with one of your 4 "
          "labels\n   (planning.md §3), then run: "
          f"python scripts/validate_dataset.py {args.out}")
    if args.sample and args.sample < n_usable:
        print(f"   (random sample of {args.sample}, seed={RANDOM_STATE} — reproducible)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
