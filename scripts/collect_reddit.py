#!/usr/bin/env python3
"""Collect PUBLIC r/anime posts/comments via Reddit's OFFICIAL API (no GPU).

This uses Reddit's sanctioned API (PRAW) — it is NOT HTML scraping. It pulls
only public submissions/comments and writes them to a CSV with the `label`
column LEFT BLANK so you annotate them yourself (collection + annotation are
your work; this tool only fetches text).

It does NOT label anything and does NOT invent text — every row is a real public
post/comment fetched from Reddit, with a permalink in `notes` for provenance.

Setup (one time):
    1. Create a Reddit "script" app: https://www.reddit.com/prefs/apps
       (click "create another app", choose type "script", any redirect URI
       e.g. http://localhost:8080). This gives you a client id + secret.
    2. Put credentials in .env (see .env.example):
         REDDIT_CLIENT_ID=...
         REDDIT_CLIENT_SECRET=...
         REDDIT_USER_AGENT=takemeter:v1 (by /u/your_username)
    3. pip install -r requirements-local.txt   (installs praw)

Usage:
    # Pull submissions across thread types into the default CSV:
    python scripts/collect_reddit.py --submissions --per-source 80

    # Also pull top-level comments from hot discussion threads:
    python scripts/collect_reddit.py --comments --per-source 60

    # Append more later (dedups against existing rows by text):
    python scripts/collect_reddit.py --submissions --per-source 40 --append

Then ANNOTATE: open data/dataset.csv and fill the `label` column with one of
your three labels (see planning.md §2), and run scripts/validate_dataset.py.
"""

import argparse
import csv
import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit(
        "❌ python-dotenv not installed. Run: pip install -r requirements-local.txt"
    )

SUBREDDIT = "anime"
DEFAULT_OUT = "data/dataset.csv"
COLUMNS = ["text", "label", "notes"]

# Minimum characters to keep a post/comment (skips "lol", removed/deleted stubs).
MIN_CHARS = 20
SKIP_BODIES = {"[removed]", "[deleted]", ""}

# Submission "sort" sources to sample across, so collection spans the thread
# types your taxonomy covers (help requests, episode/event reactions, and
# discussion). You still decide each row's label — these are just where to look.
SUBMISSION_SOURCES = ["new", "hot", "top"]


def get_reddit():
    """Build a read-only PRAW client from .env credentials."""
    load_dotenv()
    cid = os.environ.get("REDDIT_CLIENT_ID")
    secret = os.environ.get("REDDIT_CLIENT_SECRET")
    ua = os.environ.get("REDDIT_USER_AGENT")
    missing = [
        name
        for name, val in [
            ("REDDIT_CLIENT_ID", cid),
            ("REDDIT_CLIENT_SECRET", secret),
            ("REDDIT_USER_AGENT", ua),
        ]
        if not val
    ]
    if missing:
        print(
            "❌ Missing Reddit API credentials in .env: "
            + ", ".join(missing)
            + "\n   See the setup notes at the top of this script / .env.example.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import praw
    except ImportError:
        print(
            "❌ praw not installed. Run: pip install -r requirements-local.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    return praw.Reddit(
        client_id=cid,
        client_secret=secret,
        user_agent=ua,
        check_for_async=False,
    )


def clean(text: str) -> str:
    """Normalize whitespace; CSV writer handles quoting/newlines safely."""
    return " ".join((text or "").split())


def load_existing_texts(path: str) -> set:
    """Return the set of existing `text` values so --append can dedup."""
    if not os.path.exists(path):
        return set()
    seen = set()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (row.get("text") or "").strip()
            if t:
                seen.add(t)
    return seen


def collect_submissions(reddit, per_source: int):
    """Yield (text, notes) for public submissions across SUBMISSION_SOURCES.

    `text` = title + selftext (self posts) or just the title (link posts).
    """
    sub = reddit.subreddit(SUBREDDIT)
    for source in SUBMISSION_SOURCES:
        lister = {
            "new": sub.new,
            "hot": sub.hot,
            "top": lambda limit: sub.top(time_filter="month", limit=limit),
        }[source]
        for s in lister(limit=per_source):
            if getattr(s, "stickied", False):
                continue  # skip pinned/meta mod threads
            body = clean(f"{s.title} {getattr(s, 'selftext', '') or ''}")
            if len(body) < MIN_CHARS or body.lower() in SKIP_BODIES:
                continue
            notes = f"submission;{source};https://reddit.com{s.permalink}"
            yield body, notes


def collect_comments(reddit, per_source: int):
    """Yield (text, notes) for top-level comments on hot discussion threads."""
    sub = reddit.subreddit(SUBREDDIT)
    for s in sub.hot(limit=15):
        if getattr(s, "stickied", False):
            continue
        s.comments.replace_more(limit=0)
        taken = 0
        for c in s.comments:  # top-level only
            body = clean(getattr(c, "body", ""))
            if len(body) < MIN_CHARS or body.lower() in SKIP_BODIES:
                continue
            notes = f"comment;https://reddit.com{c.permalink}"
            yield body, notes
            taken += 1
            if taken >= per_source:
                break


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT, help=f"output CSV (default {DEFAULT_OUT})")
    parser.add_argument("--submissions", action="store_true", help="collect submissions")
    parser.add_argument("--comments", action="store_true", help="collect top-level comments")
    parser.add_argument(
        "--per-source",
        type=int,
        default=80,
        help="max rows per source (per sort, or per thread for comments)",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="append to existing CSV (dedups against existing text)",
    )
    args = parser.parse_args()

    if not args.submissions and not args.comments:
        print("Nothing to do: pass --submissions and/or --comments.", file=sys.stderr)
        return 2

    reddit = get_reddit()

    seen = load_existing_texts(args.out) if args.append else set()
    mode = "a" if (args.append and os.path.exists(args.out)) else "w"
    write_header = mode == "w"

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    n_written = 0
    n_dup = 0

    with open(args.out, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(COLUMNS)

        generators = []
        if args.submissions:
            generators.append(collect_submissions(reddit, args.per_source))
        if args.comments:
            generators.append(collect_comments(reddit, args.per_source))

        for gen in generators:
            for text, notes in gen:
                if text in seen:
                    n_dup += 1
                    continue
                seen.add(text)
                writer.writerow([text, "", notes])  # label intentionally BLANK
                n_written += 1

    print(f"✅ Wrote {n_written} new row(s) to {args.out} (skipped {n_dup} duplicate).")
    print("   The `label` column is BLANK on purpose — annotate it yourself:")
    print("   each row gets one of your 3 labels from planning.md §2.")
    print("   Then run: python scripts/validate_dataset.py", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
