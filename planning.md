# TakeMeter — Planning Spec

> **TakeMeter** is a fine-tuned DistilBERT text classifier that scores discourse
> quality in **r/anime**, compared against a zero-shot Groq
> `llama-3.3-70b-versatile` baseline.
>
> **This is my design document (CodePath AI201 Project 3, Milestone 2).** It must
> answer six questions with specific, committed answers — not placeholders —
> before any labeled example is collected: Community, Labels, Hard edge cases,
> Data collection plan, Evaluation metrics, and Definition of success, plus an
> AI Tool Plan. Sections still marked _TODO_ are mine to fill in; I am not
> letting tooling design my labels, collect/annotate my data, or write my
> analysis.

**Milestone 2 completion checklist (tick when each holds):**
- [ ] §1–§6 answered with specific, committed answers (no _TODO_ left)
- [ ] Label definitions precise enough two people would agree on most examples
- [ ] §6 success criteria state a numeric threshold, not "it should work well"
- [ ] AI Tool Plan makes an explicit decision on all three uses

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

Must answer: **where** I collect, **how many per label**, and **what I do if a
label is underrepresented after 200 examples.**

- **Source + method:** _TODO — r/anime, via what? (official Reddit API / manual
  copy / pushshift-style export within terms). No scraping, no fabrication._
- **Target counts:** _TODO — per-label target and total (≥200 total, aim ≥20%
  per label so no class dominates). State the per-class number you're aiming for._
- **Storage:** `data/dataset.csv` with columns `text,label,notes`. _(`notes`
  also records pre-labeling provenance — see AI Tool Plan §Annotation.)_
- **Annotation process:** _TODO — who labels, in what order, against which
  definitions (link §2), and how you keep yourself consistent over 200 rows._
- **Underrepresentation contingency (required):** _TODO — concrete plan if a
  label is <20% after 200, e.g. "targeted collection from <which threads> until
  each class ≥ N," or "merge/redefine labels per §2." Decide the rule now._

---

## 5. Evaluation metrics

Must answer: **which metrics, and why they're right for THIS task.** Accuracy
alone is not enough — say what else and why.

- **Primary metric(s):** _TODO — e.g. macro-F1. Justify: with 3 classes and
  possible imbalance, why does this metric reflect success better than raw
  accuracy for r/anime discourse?_
- **Per-class metric (required):** _TODO — precision/recall/F1 per label, and
  which class's recall/precision you care most about and why._
- **Confusion matrix:** _TODO — which specific confusion you expect and will
  inspect (e.g. label_X ↔ label_Y) and what that confusion would mean._
- **Baseline handling:** _TODO — how you treat unparseable Groq outputs (the
  local/Colab baseline excludes them and reports the count; state your stance)._
- **Same test set:** both models evaluated on the identical seeded test split
  (stratified 70/15/15, `random_state=42`) — see `scripts/baseline_groq.py`.

---

## 6. Definition of success

Must state a **specific, objectively checkable threshold** — not "it should work
well." At the end I should be able to say yes/no against these.

- **Quantitative bar:** _TODO — e.g. "fine-tuned macro-F1 ≥ 0.__ AND beats the
  Groq baseline by ≥ __ points on macro-F1." Pick real numbers._
- **Per-class floor:** _TODO — e.g. "no class below __ recall," so success isn't
  carried by one easy class._
- **"Good enough to deploy" bar:** _TODO — what performance would make this
  genuinely useful as a real r/anime community tool? Qualitative is fine here,
  but tie it to the numbers above._
- **Self-check:** are these specific enough to objectively pass/fail at the end?
  _TODO: yes/no + why._

---

## AI Tool Plan

Per Milestone 2, this section makes an **explicit decision** about the three
places AI tooling actually helps on this project. (The scaffolding/tooling
boundary below is fixed; the per-use decisions are mine.)

### A. Label stress-testing — _planned: yes_
Once my §2 definitions are drafted, I'll give the AI my label definitions + the
§3 edge case and ask it to generate 5–10 posts that sit on the boundary between
two labels. If I can't classify its outputs cleanly under my own rules, my
definitions are too loose and I'll tighten §2 **before** annotating 200 examples.
- _TODO: paste/summarize the stress-test results and any definition changes here._
- Note: these generated posts are a **test of my definitions only** — they are
  NOT added to `data/dataset.csv`.

### B. Annotation assistance — _decision: LLM pre-labels, I review every row_
I will use an LLM to **pre-label** a batch of collected r/anime posts, then
**review and correct every row myself** against my §2 definitions. The label of
record is my reviewed judgment, not the model's suggestion.
- **Tool:** _TODO — which model/tool you use for pre-labeling (e.g. Groq
  llama-3.3-70b-versatile, to match the baseline)._
- **Tracking convention:** the `notes` column flags provenance so it's auditable
  and disclosable — e.g. `prelabeled:groq;changed` if I overrode the suggestion,
  `prelabeled:groq;kept` if I agreed, blank/`manual` if I labeled from scratch.
  _TODO: confirm the exact tokens you'll use._
- **Disclosure:** I will report in the README AI usage section that rows were
  LLM-pre-labeled and 100% human-reviewed, with the count changed vs. kept.
- _Guardrail:_ pre-labeling could bias my annotations toward the model. I will
  review against the definitions, not the suggestion, and (stretch) an
  inter-annotator check would catch systematic drift.

### C. Failure analysis — _planned: yes, with my own verification_
After evaluation, I'll give the AI my list of wrong predictions (text, true,
predicted) and ask it to surface **patterns** (e.g. "misclassifies short hype as
X," "confuses label_Y with label_Z on spoiler-tagged posts").
- **What I'll look for:** systematic confusions, length effects, keyword
  shortcuts vs. the intended distinction (the learned-vs-intended question).
- **Verification:** any pattern the AI proposes I confirm myself against actual
  examples before it goes in the evaluation report — the AI proposes, I verify.

---

### Fixed boundary (not negotiable)

**AI tooling is used for:** repo scaffolding, local tooling
(`scripts/validate_dataset.py`, `scripts/baseline_groq.py`), and the three uses
above (stress-testing, pre-labeling-with-review, failure-pattern surfacing).

**Entirely my own work (not AI-authored):** label design and definitions, the
final label of record on every row, the baseline system prompt, and all
analysis, the evaluation writeup, and reflections.
