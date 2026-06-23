# TakeMeter — Planning

> **TakeMeter** is a fine-tuned DistilBERT text classifier that scores discourse
> quality in an online community, compared against a zero-shot Groq
> `llama-3.3-70b-versatile` baseline.
>
> This document is **your** planning work. Everything below is a placeholder —
> fill in each section with your own decisions. Do not let tooling write your
> label design, data collection, annotation, or analysis for you.

---

## 1. Community  — Milestone 1

**Community:** r/anime (general anime subreddit)

<!-- TODO (Milestone 1, ~2-3 sentences — YOUR words):
     - Name + link the community (https://www.reddit.com/r/anime/).
     - Why is its discourse a good fit? r/anime mixes episode-discussion
       reactions, recommendation threads, news, and deeper critique — so
       "quality of discourse" varies a lot, which is what makes it classifiable.
     - Confirm you can collect 200+ PUBLIC posts/comments and that doing so is
       allowed (read Reddit's terms / use the official API or manual copy;
       no scraping, no fabrication).
     - Roughly how active / how much can you realistically gather?

     Checkpoint reminder: before you finalize labels, READ 30-40 real r/anime
     posts and note the patterns you actually see. Don't design from memory. -->

_TODO: write your 2-3 sentence community description here._

---

## 2. Labels  — Milestone 1 (3 labels)

> Required properties (verify each holds): **mutually exclusive** (a post fits
> exactly one), **exhaustive enough** (you can label ≥90% with no catch-all
> "other"), and **grounded in r/anime norms** (the distinction matters to people
> who actually post there). Aim for **≥20% of examples per label**.
>
> Label strings here MUST match `LABEL_MAP` in `scripts/validate_dataset.py`,
> the README taxonomy table, and the Colab notebook.

### Label 1 — `TODO_label_1`
- **One-sentence definition:** _TODO_
- **Clear example A (a real-ish post in your own words):** _TODO_
- **Clear example B:** _TODO_
- **An uncertain case (a post you're NOT sure belongs here):** _TODO — this one
  matters most; it forces you to sharpen the boundary._

### Label 2 — `TODO_label_2`
- **One-sentence definition:** _TODO_
- **Clear example A:** _TODO_
- **Clear example B:** _TODO_
- **An uncertain case:** _TODO_

### Label 3 — `TODO_label_3`
- **One-sentence definition:** _TODO_
- **Clear example A:** _TODO_
- **Clear example B:** _TODO_
- **An uncertain case:** _TODO_

<!-- Mutual-exclusivity check (do this, write the answer):
     Pick ~5 random r/anime posts. Can you assign each to exactly ONE label
     without ambiguity most of the time? If two labels keep overlapping, merge
     them or redefine the boundary, then update the blocks above. -->

**Mutual-exclusivity self-check result:** _TODO_

---

## 3. Hard edge cases  — Milestone 1 checkpoint

> The checkpoint requires you to name the **single hardest** edge case — a post
> type that genuinely sits between two of your labels — and state the **decision
> rule** you'll use so annotation stays consistent. Find one such REAL post in
> r/anime before you commit to your labels.

### Hardest edge case (required)
- **The post / post type:** _TODO — describe a real borderline r/anime post._
- **Which two labels it could belong to:** _TODO_
- **Your decision rule (one sentence that resolves it):** _TODO_
- **How you'd label THIS post under that rule, and why:** _TODO_

### Other edge cases + tie-breaking rules (optional but recommended)
<!-- Kinds to think about for an anime community (these are prompts, not answers):
     - sarcasm / ironic praise that flips intent
     - short low-effort hype vs. a concise but substantive take
     - spoiler-tagged analysis vs. plain reaction
     - "peak fiction" / meme one-liners
     - quoting a bad take to criticize it
     - off-topic but high-effort (e.g., production/industry tangents) -->

_TODO: list any other edge cases and how you'll decide them._

---

## 4. Data collection plan

<!-- TODO: How will you collect and annotate data YOURSELF?
     - source + method (manual copy, official API, export, etc.)
     - target count per class and total (aim for a balanced, sufficient set)
     - who annotates and how you'll check consistency
     - how you store it (data/dataset.csv with text,label,notes)
     Remember: no scraping/fabrication — collection and annotation are your work. -->

_TODO: describe your collection and annotation plan here._

---

## 5. Evaluation metrics

<!-- TODO: How will you judge fine-tuned DistilBERT vs. the Groq baseline?
     - which metrics (accuracy, macro-F1, per-class precision/recall, ...)
     - confusion matrix + what specific confusions you'll inspect
     - how you'll handle unparseable baseline outputs -->

_TODO: define your metrics and comparison method here._

---

## 6. Definition of success

<!-- TODO: What outcome would make this project a success?
     Be concrete: e.g., a target macro-F1, or "fine-tuned beats baseline by X on
     class Y," or a qualitative bar for the learned-vs-intended reflection. -->

_TODO: state your success criteria here._

---

## AI Tool Plan

<!-- TODO: Document how you used AI tooling on this project and where you drew
     the line. The scaffolding/tooling boundary is fixed (below); fill in the
     specifics of what you asked for and what you kept as your own work. -->

**What AI tooling was used for (allowed):**
- Repo scaffolding (this file's structure, README skeleton, configs)
- Local validation tooling (`scripts/validate_dataset.py`)
- Local baseline harness (`scripts/baseline_groq.py`)

**What remains entirely my own work (not AI-generated):**
- Label design and definitions
- Data collection and annotation
- The system prompt for the baseline
- All analysis, the evaluation writeup, and reflections

_TODO: add any specifics about tools/prompts you used and your review process._
