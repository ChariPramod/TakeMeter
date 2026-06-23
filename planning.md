# TakeMeter — Planning

> **TakeMeter** is a fine-tuned DistilBERT text classifier that scores discourse
> quality in an online community, compared against a zero-shot Groq
> `llama-3.3-70b-versatile` baseline.
>
> This document is **your** planning work. Everything below is a placeholder —
> fill in each section with your own decisions. Do not let tooling write your
> label design, data collection, annotation, or analysis for you.

---

## 1. Community

<!-- TODO: Which online community are you classifying discourse from?
     Name it, link it, and explain why it's a good fit:
     - Is the discourse varied enough to be interesting to classify?
     - Are posts publicly available and OK to collect per the source's terms?
     - Roughly how active is it / how many posts can you realistically gather? -->

_TODO: describe the community here._

---

## 2. Labels

<!-- TODO: Define your label taxonomy for "discourse quality."
     For EACH label give:
     - the exact label string (this must match LABEL_MAP in validate_dataset.py)
     - a one-sentence definition
     - 1-2 short illustrative descriptions (in your own words; do NOT paste
       fabricated example posts)
     Keep the set small and mutually exclusive enough to annotate consistently. -->

_TODO: list your labels and their definitions here._

---

## 3. Hard edge cases

<!-- TODO: List the cases that are genuinely hard to label and explain how you
     will decide them. Examples of *kinds* of edge cases to think about
     (not answers — your call):
     - sarcasm / irony that flips intent
     - short low-effort posts vs. concise good ones
     - off-topic but high-quality
     - quoting bad content to criticize it
     Write your tie-breaking rules so annotation stays consistent. -->

_TODO: enumerate edge cases and your tie-breaking rules here._

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
