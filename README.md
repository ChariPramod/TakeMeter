# TakeMeter

A fine-tuned **DistilBERT** text classifier that scores **discourse quality** in
an online community, compared against a zero-shot **Groq
`llama-3.3-70b-versatile`** baseline.

> **Where the GPU work happens:** fine-tuning runs on **Google Colab (free T4
> GPU)** using the provided starter notebook — _not_ locally. This repo holds
> everything *outside* the notebook plus local tooling to de-risk Colab runs
> (dataset validation and the Groq baseline). See [CLAUDE.md](CLAUDE.md) for the
> project rules.

---

## Overview

<!-- TODO: 2-4 sentences for a reader who hasn't seen planning.md. What does
     TakeMeter do, for which community (r/wallstreetbets), what are the 4 labels
     at a glance, and what question does the fine-tuned-vs-baseline comparison
     answer? -->

_TODO_

> **Demo video:** _TODO — link (3–5 min: 3–5 posts classified with label +
> confidence, one correct prediction narrated, one wrong prediction narrated, and
> a walkthrough of this evaluation report)._

---

## Data collection

**Source.** Downloaded public r/wallstreetbets dataset (`data/reddit_wsb.csv`,
~53k posts). _TODO: add the source/link you downloaded it from._ Cleaned and
sampled into `data/dataset.csv` with
[scripts/clean_wsb.py](scripts/clean_wsb.py) (`text = title + body`, deduped,
seeded sample); see [Local setup](#local-setup).

**Annotation.** _TODO: describe how you labeled — read each post against the
planning.md §3 definitions; note whether you used LLM pre-labeling with review
(disclose in [AI usage](#ai-usage) if so)._

**Final label distribution** (fill from `validate_dataset.py` output):

| Label | Count |
|-------|------:|
| `trade_analysis` | _TODO_ |
| `market_reaction_or_hype` | _TODO_ |
| `meme_or_shitpost` | _TODO_ |
| `community_meta_or_news` | _TODO_ |
| **Total** | _TODO (≥200)_ |

<!-- Checkpoint: no single label > 70% of the dataset. -->

**3 genuinely difficult examples** (full list of edge cases in
[planning.md](planning.md) §5):

1. _TODO: the post (excerpt), which two labels it sat between, what you decided & why._
2. _TODO_
3. _TODO_

---

## Label taxonomy

Community: **r/wallstreetbets**. Four labels (see [planning.md](planning.md) §3
for full definitions, examples, and the edge-case decision rule). These must
match `LABEL_MAP` in [scripts/validate_dataset.py](scripts/validate_dataset.py)
and the Colab notebook.

| Label | Definition (short — see [planning.md](planning.md) §3 for full) |
|-------|------------|
| `trade_analysis` | Primarily explains/justifies/evaluates a stock, option, market move, or strategy using reasoning, evidence, numbers, or a clear thesis. |
| `market_reaction_or_hype` | Primarily an emotional reaction to market movement — hype, celebration, panic, or encouragement to buy/hold/sell, without substantial analysis. |
| `meme_or_shitpost` | Primarily humor, sarcasm, slang, or absurdity for entertainment rather than serious trading discussion. |
| `community_meta_or_news` | Primarily about the subreddit, moderation, daily threads, media attention, rules, or external WSB news rather than a personal trade. |

---

## Model + training

- **Base model:** `distilbert-base-uncased` with a 4-class classification head.
- **Split:** stratified 70 / 15 / 15 (train / val / test), `random_state=42`,
  done in the notebook. Test set sizes: _TODO from Section 2 output._
- **Tokenization:** max length 256.
- **Hyperparameters (notebook defaults):** 3 epochs, learning rate 2e-5, train
  batch size 16, weight decay 0.01, warmup 50 steps.
- **Compute:** Google Colab free **T4 GPU**.

<!-- TODO: If you changed ANY hyperparameter from the defaults above, state what
     you changed and WHY. If you kept the defaults, say so. -->

_TODO: note any hyperparameter changes (or "kept defaults")._

---

## Evaluation report

All numbers below come from running the Colab notebook on the **same locked test
set** (`evaluation_results.json` + `confusion_matrix.png`, committed to this
repo). Fill every `_TODO_` from your actual output — do not estimate.

### Headline metrics

| Model | Accuracy | Macro-F1 | Unparseable |
|-------|---------:|---------:|------------:|
| Groq zero-shot baseline (`llama-3.3-70b-versatile`) | _TODO_ | _TODO_ | _TODO_ / _TODO_ |
| Fine-tuned DistilBERT | _TODO_ | _TODO_ | — |

### Per-class metrics — Groq baseline

<!-- From the Section 5 classification_report. -->

| Label | Precision | Recall | F1 |
|-------|----------:|-------:|---:|
| `trade_analysis` | _TODO_ | _TODO_ | _TODO_ |
| `market_reaction_or_hype` | _TODO_ | _TODO_ | _TODO_ |
| `meme_or_shitpost` | _TODO_ | _TODO_ | _TODO_ |
| `community_meta_or_news` | _TODO_ | _TODO_ | _TODO_ |

### Per-class metrics — Fine-tuned DistilBERT

<!-- From the Section 4 classification_report. -->

| Label | Precision | Recall | F1 |
|-------|----------:|-------:|---:|
| `trade_analysis` | _TODO_ | _TODO_ | _TODO_ |
| `market_reaction_or_hype` | _TODO_ | _TODO_ | _TODO_ |
| `meme_or_shitpost` | _TODO_ | _TODO_ | _TODO_ |
| `community_meta_or_news` | _TODO_ | _TODO_ | _TODO_ |

### Confusion matrix — Fine-tuned DistilBERT

Text version (the `confusion_matrix.png` is committed as a supplementary copy).
Rows = true label, columns = predicted label; the diagonal is correct.

| true \ pred | trade_analysis | market_reaction_or_hype | meme_or_shitpost | community_meta_or_news |
|-------------|---------:|---------:|---------:|---------:|
| **trade_analysis** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **market_reaction_or_hype** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **meme_or_shitpost** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **community_meta_or_news** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

### Did it hit the success criteria?

Check against [planning.md](planning.md) §8 (accuracy ≥ 0.75, macro-F1 ≥ 0.70,
every per-class F1 ≥ 0.65, `trade_analysis` precision ≥ 0.75):

- _TODO: state met / not-met for each clause, citing the numbers above._

### Discussion

<!-- TODO: What do the numbers + matrix show? Where does fine-tuning beat (or
     lose to) the baseline, and by how much? -->

_TODO_

---

## Failure analysis (3 analyzed errors)

Before writing this, you may paste your misclassified examples into an LLM to
surface patterns — then verify each pattern yourself by re-reading the cases
(disclose this in [AI usage](#ai-usage)). "The model got it wrong" is not
analysis; answer the guiding questions for each.

**Wrong predictions reviewed:** _TODO / TODO total test examples._

For each of the 3 examples below, fill: the post (excerpt), true vs. predicted
label, the model's confidence, and the analysis.

### Failure 1
- **Post:** _TODO_
- **True → Predicted (confidence):** _TODO_ → _TODO_ (_TODO_)
- **Which boundary failed?** _TODO — which label pair, and is it the dominant
  off-diagonal in the confusion matrix?_
- **Why is that boundary hard?** _TODO — ambiguous language, sarcasm, short post,
  topic-signals-one-label-but-structure-signals-another, etc._
- **Labeling problem or data/prompt problem?** _TODO — did you label similar
  posts consistently? If yes, it's the data distribution / boundary; if no, it's
  annotation inconsistency._
- **What would fix it?** _TODO_

### Failure 2
- **Post:** _TODO_
- **True → Predicted (confidence):** _TODO_ → _TODO_ (_TODO_)
- **Which boundary failed?** _TODO_
- **Why is that boundary hard?** _TODO_
- **Labeling problem or data/prompt problem?** _TODO_
- **What would fix it?** _TODO_

### Failure 3
- **Post:** _TODO_
- **True → Predicted (confidence):** _TODO_ → _TODO_ (_TODO_)
- **Which boundary failed?** _TODO_
- **Why is that boundary hard?** _TODO_
- **Labeling problem or data/prompt problem?** _TODO_
- **What would fix it?** _TODO_

---

## Sample classifications

3–5 example posts run through the **fine-tuned** model, each with the predicted
label and confidence. (From the Section 4 output / wrong-prediction cell.)

| # | Post (excerpt) | Predicted label | Confidence | Correct? |
|---|----------------|-----------------|-----------:|:--------:|
| 1 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| 2 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| 3 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| 4 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| 5 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

**Why one correct prediction is reasonable:** _TODO — pick a correctly-predicted
row above and explain in a sentence why the label fits the post's content._

---

## Reflection: learned vs. intended

<!-- This is a HIGHER-LEVEL observation than the failure list above: the gap
     between your label DEFINITIONS and what the model's decision boundary
     actually captures. -->

- **What did the model overfit to?** _TODO — surface cues like ticker symbols,
  ALL-CAPS/emoji, post length, specific keywords ("DD", "moon", "HOLD")?_
- **What did it miss?** _TODO — which intended distinction didn't it learn?_
- **Overall:** did it learn *discourse purpose* (your intent) or a correlated
  proxy? _TODO — cite specific evidence from the errors/confusion matrix._

_TODO: write this yourself._

---

## Spec reflection

- **One way the spec helped:** _TODO — name a specific requirement that guided a
  decision (e.g. the "no label > 70%" rule pushing you to targeted top-up
  sampling, or the per-class-F1 success bar shaping your metric choice)._
- **One way my implementation diverged, and why:** _TODO — e.g. you adjusted the
  sample size, re-scoped the community, or changed a hyperparameter; say why._

---

## AI usage

The fixed boundary is in [CLAUDE.md](CLAUDE.md) and [planning.md](planning.md) §9:
AI was used for repo scaffolding, local tooling
([clean_wsb.py](scripts/clean_wsb.py),
[validate_dataset.py](scripts/validate_dataset.py),
[baseline_groq.py](scripts/baseline_groq.py)), and the three planned uses
(label stress-testing, optional pre-labeling with review, failure-pattern
surfacing). Label design, the final label on every row, the system prompt
content (transcribed from my own §3 definitions), and all analysis/reflections
are my own work.

**Specific instances** (describe ≥2: what you directed the tool to do, what it
produced, what you changed/overrode):

1. _TODO — e.g. "Directed the AI to scaffold the repo + cleaning/validation
   tooling for a downloaded WSB dataset. It produced clean_wsb.py and the README
   structure; I supplied all label definitions and reviewed/edited X."_
2. _TODO — e.g. failure-pattern surfacing: "I pasted my misclassified examples
   and asked for common themes; it suggested <pattern>. I verified by re-reading
   and kept/discarded <which> because <why>."_

**Annotation disclosure:** _TODO — state whether you used LLM pre-labeling. If
yes: which model, that you reviewed and corrected EVERY row, and how many
suggestions you changed vs. kept. If no: state that all labels were assigned
manually._

---

## Repo layout

```
TakeMeter/
├── planning.md              # planning spec (your work)
├── README.md                # this file
├── CLAUDE.md                # project rules for AI sessions
├── requirements-local.txt   # deps for local tooling (no GPU)
├── .env.example             # copy to .env, add GROQ_API_KEY
├── data/
│   ├── dataset_template.csv # column template: text,label,notes
│   ├── reddit_wsb.csv       # the downloaded public WSB dataset (gitignored)
│   └── dataset.csv          # cleaned + sampled + YOUR annotations (committed)
├── scripts/
│   ├── clean_wsb.py         # clean/sample reddit_wsb.csv -> dataset.csv (no labels)
│   ├── validate_dataset.py  # pre-Colab dataset sanity check (no GPU)
│   └── baseline_groq.py     # local zero-shot Groq baseline (no GPU)
├── AI201 Project 3 Takemeter Starter.ipynb  # Colab fine-tuning notebook
├── evaluation_results.json  # downloaded from Colab (Section 6) — commit it
└── confusion_matrix.png     # downloaded from Colab (Section 4) — commit it
```

## Local setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-local.txt
cp .env.example .env        # then add GROQ_API_KEY
```

### 1. Clean + sample the downloaded WSB dataset

Put the downloaded public dataset at `data/reddit_wsb.csv`, then build a cleaned,
deduped pool with `text = title + body` and the `label` column **left blank** for
you to annotate:

```bash
python scripts/clean_wsb.py --in data/reddit_wsb.csv --out data/dataset.csv --sample 300
```

Cleaning only formats/filters real rows — it does **not** assign labels.

### 2. Annotate, validate, baseline

```bash
# Open data/dataset.csv and fill the `label` column with one of your 4 labels
# (planning.md §3). Then validate before uploading to Colab:
python scripts/validate_dataset.py data/dataset.csv

# Run the zero-shot baseline locally (after filling in SYSTEM_PROMPT):
python scripts/baseline_groq.py data/dataset.csv
```

### 3. Fine-tune + evaluate on Colab (Milestones 4–6)

1. Open `AI201 Project 3 Takemeter Starter.ipynb` in Colab; set runtime to
   **T4 GPU**.
2. **Section 1–2:** run; upload `data/dataset.csv` when prompted (LABEL_MAP and
   the split are already set for the 4 WSB labels).
3. **Section 5 (baseline, M4):** add your Groq key (Colab Secrets); the
   `SYSTEM_PROMPT` is already filled from planning.md §3. Run → baseline metrics.
4. **Section 3–4 (fine-tune + eval, M5):** run → per-class metrics +
   `confusion_matrix.png`.
5. **Section 6:** run → `evaluation_results.json`. Download both files, drop them
   in the repo root, and copy the numbers into the [Evaluation report](#evaluation-report).
