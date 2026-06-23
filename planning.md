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

- **Source + method:** r/anime (https://www.reddit.com/r/anime/). _TODO —
  confirm your exact collection method (official Reddit API via a registered app,
  or manual copy of public posts/comments) and that it respects Reddit's terms.
  No automated scraping, no fabricated rows._
- **Target counts:** **300 examples total, ~100 per label** across 3 classes.
  This is well above the 200 minimum and keeps every class far above the 20%
  floor, with buffer for rows dropped during validation (empty/duplicate/short).
- **Storage:** `data/dataset.csv` with columns `text,label,notes`. The `notes`
  column also records pre-labeling provenance — see AI Tool Plan §B.
- **Annotation process:** _TODO — label against the §2 definitions; with the
  pre-label-and-review workflow (§B), the LLM proposes a label, I confirm or
  override every row, and the final label is my judgment. Note how you stay
  consistent across 300 rows (e.g. re-read definitions periodically; revisit any
  row you hesitate on)._
- **Underrepresentation contingency:** if any class is below the 20% floor
  (i.e. < 60 rows) after the first pass, do **targeted collection** — pull
  additional posts from thread types known to produce that class until it reaches
  ~100 — rather than down-sampling the others. If a class stays hard to fill, it
  is a signal the boundary in §2 is wrong; merge/redefine per §2 instead of
  forcing thin data. _TODO: confirm which thread types you'll target for top-up._

---

## 5. Evaluation metrics

Must answer: **which metrics, and why they're right for THIS task.** Accuracy
alone is not enough — say what else and why.

- **Primary metric: macro-F1.** Averaging F1 equally across the three classes
  (rather than weighting by frequency) means a class that drifts below the 20%
  floor still counts fully toward the score. Raw accuracy can look high while
  one r/anime discourse type is barely recognized, so accuracy alone would hide
  exactly the failure I care about; macro-F1 won't.
- **Per-class precision / recall / F1 (required).** Reported for every label so
  I can see *which* class the model handles worst — not just an aggregate. I care
  most about **recall on the minority/most-confused class** (it's the one most
  likely to be silently dropped). _TODO: name which of your 3 labels you most
  want high recall on, once defined._
- **Confusion matrix.** 3×3, true (rows) × predicted (cols). I'll inspect which
  specific pair gets confused; a heavy off-diagonal between two labels means
  their §2 boundary is blurry in practice. _TODO: name the pair you expect to be
  most confused, given your definitions._
- **Baseline handling:** unparseable Groq outputs are **excluded from the metric
  and reported as a separate count** (the local/Colab harness already does this).
  A high unparseable count is itself a finding about the zero-shot prompt, so I
  report it rather than silently dropping it.
- **Same test set:** both models are evaluated on the identical seeded test split
  (stratified 70/15/15, `random_state=42`) — see `scripts/baseline_groq.py`,
  which reproduces the notebook's split exactly so local == Colab.

---

## 6. Definition of success

Must state a **specific, objectively checkable threshold** — not "it should work
well." At the end I should be able to say yes/no against these.

- **Quantitative bar:** the fine-tuned model reaches **macro-F1 ≥ 0.70** on the
  test set **AND** beats the zero-shot Groq baseline by **≥ 0.05 macro-F1**.
- **Per-class floor:** **no class has recall < 0.55**, so success can't be
  carried by one easy class while another is effectively ignored.
- **"Good enough to deploy" bar:** at macro-F1 ≥ 0.70 with no collapsed class,
  the classifier is useful as an *assistive* signal in a real r/anime tool (e.g.
  flagging/sorting discourse types for a human), not as a fully automated
  moderator — three-way subjective discourse labeling on ~300 examples won't be
  reliable enough to act on without review, and the success bar reflects that.
- **Self-check — are these objectively pass/fail?** Yes. Each clause is a number
  the evaluation in §5 produces directly (macro-F1, the baseline delta, and the
  minimum per-class recall), so at the end I can mark each as met/not-met without
  judgment calls. _(I may tighten these after seeing the baseline numbers, and
  will note any change here.)_

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
