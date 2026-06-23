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

<!-- Draft below is a factual summary — edit into your own voice. -->

TakeMeter classifies the **purpose** of a r/wallstreetbets post into one of four
discourse types — `trade_analysis`, `market_reaction_or_hype`, `meme_or_shitpost`,
or `community_meta_or_news` — to measure how a community's discussion divides
between substantive trading analysis and everything else. It compares a
**fine-tuned DistilBERT** classifier (trained on 305 hand-labeled examples)
against a **zero-shot Groq `llama-3.3-70b-versatile`** baseline on the same test
set, to see how much a small fine-tuned model can close the gap to a large
general LLM on a subjective, imbalanced, 4-way task.

_TODO: tweak wording / add your one-line takeaway._

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

**Annotation.** Each row was read and labeled against the [planning.md](planning.md)
§3 definitions. Started from a 300-row random sample; two thin classes were then
topped up by surfacing keyword candidates (planning §6 contingency) and labeling
those by hand — keyword search only *found* candidates, it never assigned labels.
_TODO: note whether any LLM pre-labeling was used; disclose in [AI usage](#ai-usage) if so._

**Final label distribution** (437 rows; verified with `validate_dataset.py`, no
single label > 70%):

| Label | Count | Share |
|-------|------:|------:|
| `market_reaction_or_hype` | 163 | 37.3% |
| `trade_analysis` | 113 | 25.9% |
| `community_meta_or_news` | 108 | 24.7% |
| `meme_or_shitpost` | 53 | 12.1% |
| **Total** | **437** | 100% |

`meme_or_shitpost` is the smallest class — genuine memes are rarer in WSB than
hype — so its per-class metrics are the least certain; this is noted in the
evaluation discussion.

**3 genuinely difficult examples** (full detail + decision rules in
[planning.md](planning.md) §5):

1. **"Marble ETF" post** (`o64enf`) — DD *structure* but intentionally absurd
   method → `meme_or_shitpost` (a real ticker/DD format doesn't make it analysis).
2. **GME/AMC float-ownership squeeze math** (`mcf7u1`) — rough numbers + a
   concrete market mechanism, despite "hold forever" tone → `trade_analysis`.
3. **AMD YOLO update** (`lgx0fn`) — real positions but the body is comedic
   performance, not reasoning → `meme_or_shitpost`.

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
- **Split:** stratified 70 / 15 / 15, `random_state=42` (notebook). Sizes:
  **305 train / 66 validation / 66 test**.
- **Tokenization:** max length 256.
- **Compute:** Google Colab free **T4 GPU**.

**Hyperparameters and the changes I made.** The notebook defaults (3 epochs,
unweighted loss, select-best-by-accuracy) produced a model that **collapsed onto
the two largest classes** — `meme_or_shitpost` and `community_meta_or_news` both
scored F1 0.00, and overall accuracy (0.561) was far below the baseline. I made
three changes to fix the minority-class collapse:

| Change | From → To | Why |
|--------|-----------|-----|
| Loss | unweighted → **inverse-frequency class-weighted** cross-entropy | Penalize errors on rare classes so they aren't ignored. Weights from the train split only (no test leakage): meme ≈ 2.06, others ≈ 0.67–1.02. |
| Epochs | 3 → **6** | 305 training examples need more passes to learn the minority classes; `load_best_model_at_end` guards overfitting. |
| Model selection | best by `accuracy` → best by **`macro_f1`** | Accuracy rewards predicting the majority class; macro-F1 forces all 4 classes to matter. |

Learning rate (2e-5), batch size (16), weight decay (0.01), warmup (50) kept at
defaults. _TODO (optional): if you re-tune further, note it here._

---

## Evaluation report

Both models evaluated on the same locked **66-example test set** (after the
class-weighting fix; see [Model + training](#model--training)).

> ⚠️ **Baseline caveat — read before comparing.** The Groq baseline run hit the
> `llama-3.3-70b-versatile` **daily token rate limit** partway through, so **7 of
> 66** test examples returned errors and counted as unparseable. The baseline
> metrics below are therefore computed on only **59/66** examples, while the
> fine-tuned metrics use all 66. **The two are not a perfectly matched
> comparison.** _TODO (recommended): re-run Section 5 after the limit resets so
> the baseline covers all 66, then update these numbers._

### Headline metrics

| Model | Accuracy | Macro-F1 | Scored on | Unparseable |
|-------|---------:|---------:|:---------:|------------:|
| Groq zero-shot baseline (`llama-3.3-70b-versatile`) | 0.847 | 0.82 | 59 / 66 | 7 |
| Fine-tuned DistilBERT (class-weighted, 6 epochs) | 0.742 | 0.70 | 66 / 66 | — |

### Per-class metrics — Groq baseline (on 59 parseable examples)

| Label | Precision | Recall | F1 | Support |
|-------|----------:|-------:|---:|--------:|
| `trade_analysis` | 0.88 | 0.94 | 0.91 | 16 |
| `market_reaction_or_hype` | 0.81 | 0.96 | 0.88 | 23 |
| `meme_or_shitpost` | 0.83 | 0.71 | 0.77 | 7 |
| `community_meta_or_news` | 0.89 | 0.62 | 0.73 | 13 |
| **macro avg** | 0.85 | 0.81 | **0.82** | 59 |

### Per-class metrics — Fine-tuned DistilBERT (on all 66 examples)

| Label | Precision | Recall | F1 | Support |
|-------|----------:|-------:|---:|--------:|
| `trade_analysis` | 0.71 | 1.00 | 0.83 | 17 |
| `market_reaction_or_hype` | 0.86 | 0.72 | 0.78 | 25 |
| `meme_or_shitpost` | 0.57 | 0.50 | 0.53 | 8 |
| `community_meta_or_news` | 0.71 | 0.62 | 0.67 | 16 |
| **macro avg** | 0.71 | 0.71 | **0.70** | 66 |

### Confusion matrix — Fine-tuned DistilBERT

Rows = true label, columns = predicted label; the diagonal is correct. Counts
below are reconstructed from the per-class metrics + the printed wrong-prediction
list; **two of the 17 errors were truncated in the notebook output**, so two
off-diagonal cells are marked `?` — read the exact values off the committed
`confusion_matrix.png` and replace the `?`s.

| true \ pred | trade_analysis | market_reaction_or_hype | meme_or_shitpost | community_meta_or_news |
|-------------|---------:|---------:|---------:|---------:|
| **trade_analysis** | 17 | 0 | 0 | 0 |
| **market_reaction_or_hype** | 1 | 18 | 2 | 3 (+1 `?`) |
| **meme_or_shitpost** | 0 | 3 | 4 | 1 |
| **community_meta_or_news** | 5 | 0 | 0 | 10 (+1 `?`) |

(Confirmed diagonal: 17 / 18 / 4 / 10 = 49 correct of 66 = 0.742 accuracy.)

### Did it hit the success criteria?

Against [planning.md](planning.md) §8:

| Criterion | Target | Fine-tuned result | Met? |
|-----------|--------|-------------------|:----:|
| Accuracy | ≥ 0.75 | 0.742 | ❌ (just under) |
| Macro-F1 | ≥ 0.70 | 0.70 | ✅ |
| Every per-class F1 | ≥ 0.65 | meme = 0.53 | ❌ |
| `trade_analysis` precision | ≥ 0.75 | 0.71 | ❌ |
| Beats Groq baseline | yes | loses 0.742 vs 0.847 | ❌ |

So the fine-tuned model **met the macro-F1 bar but did not beat the baseline**
and missed three of the five clauses. _TODO: add a sentence on how you read this
overall (e.g. respectable for 305 training examples, but a 70B zero-shot LLM is a
hard baseline to beat on a 4-way subjective task)._

### Discussion

The class-weighting fix worked: it rescued the two minority classes from F1 0.00
(broken run) to **0.53 (meme)** and **0.67 (community_meta)**, lifting macro-F1
from 0.35 → 0.70. _TODO: expand — which boundary still drives most errors (see
the confusion matrix: `community_meta_or_news → trade_analysis` = 5, and
`market_reaction_or_hype` scatters into all three others), and why the fine-tuned
model still trails the zero-shot baseline._

<!-- TODO: also discuss `trade_analysis` recall = 1.00 with precision 0.71 — the
     model over-predicts trade_analysis (it's the catch-all for anything with
     tickers/reasoning-like structure). Is that a labeling boundary issue or a
     data issue? -->

_TODO: finish the discussion in your own words._

---

## Failure analysis (3 analyzed errors)

Before writing this, you may paste your misclassified examples into an LLM to
surface patterns — then verify each pattern yourself by re-reading the cases
(disclose this in [AI usage](#ai-usage)). "The model got it wrong" is not
analysis; answer the guiding questions for each.

**Wrong predictions reviewed:** _TODO / TODO total test examples._

**Wrong predictions reviewed:** 17 / 66 test examples. The three below are real
errors from the run (text/labels/confidence are filled in); the **analysis is
yours to write** — answer each guiding question.

### Failure 1 — the dominant error pattern
- **Post:** *"What broker to use now? Once the squeeze is over in GME and I feel comfortable moving my money I'm leaving both RH and TDA. What brokers would you recommend…"*
- **True → Predicted (confidence):** `community_meta_or_news` → `trade_analysis` (0.57)
- **Which boundary failed?** `community_meta_or_news` → `trade_analysis` — this is
  the **largest off-diagonal** (5 of 16 community_meta posts went to
  trade_analysis).
- **Why is that boundary hard?** _TODO — the post mentions tickers (GME) and
  brokers/positions, so the surface looks like trading even though the intent is a
  platform/community question. Is it the ticker presence?_
- **Labeling problem or data/prompt problem?** _TODO_
- **What would fix it?** _TODO_

### Failure 2 — a meme miss
- **Post:** *"I feel retarded as f***, is AMC going to the moon or am I fuk"*
- **True → Predicted (confidence):** `meme_or_shitpost` → `market_reaction_or_hype` (0.45)
- **Which boundary failed?** `meme_or_shitpost` → `market_reaction_or_hype` (the
  meme class's most common confusion; 3 of 8 memes went to hype).
- **Why is that boundary hard?** _TODO — short, slang-heavy, "to the moon" reads
  as hype but the intent is a self-deprecating joke. Low confidence (0.45)._
- **Labeling problem or data/prompt problem?** _TODO — note that meme has only
  ~37 train / 8 test examples._
- **What would fix it?** _TODO_

### Failure 3 — hype vs. analysis
- **Post:** *"All The Fuckery Only Galvanizes Us More… What the shorts aren't realizing is th[at]…"*
- **True → Predicted (confidence):** `market_reaction_or_hype` → `trade_analysis` (0.46)
- **Which boundary failed?** `market_reaction_or_hype` → `trade_analysis`.
- **Why is that boundary hard?** _TODO — it has an argument-like structure
  ("what the shorts aren't realizing") wrapped around what is really a rallying
  cry. Relates to your planning §5 hardest edge case._
- **Labeling problem or data/prompt problem?** _TODO_
- **What would fix it?** _TODO_

---

## Sample classifications

3–5 example posts run through the **fine-tuned** model, each with the predicted
label and confidence. Rows 1–3 are real misclassifications from the run (verified
text + confidence). For the **correct** examples (rows 4–5) the model didn't
print text for correct cases, so pull two from the notebook — e.g. re-run a small
cell printing correct predictions, or add `print(test_df.iloc[idx]['text'])` for
indices where pred == true.

| # | Post (excerpt) | Predicted label | Confidence | Correct? |
|---|----------------|-----------------|-----------:|:--------:|
| 1 | "What broker to use now? … leaving both RH and TDA. What brokers would you recommend" | `trade_analysis` | 0.57 | ❌ (true: community_meta_or_news) |
| 2 | "I feel retarded as f***, is AMC going to the moon or am I fuk" | `market_reaction_or_hype` | 0.45 | ❌ (true: meme_or_shitpost) |
| 3 | "Us little guys are holding too!! Numbers red pretty 🦍🦍💎💎👐👐🚀🚀🚀" | `meme_or_shitpost` | 0.46 | ❌ (true: market_reaction_or_hype) |
| 4 | _TODO: a correctly-predicted post_ | _TODO_ | _TODO_ | ✅ |
| 5 | _TODO: a correctly-predicted post_ | _TODO_ | _TODO_ | ✅ |

**Why one correct prediction is reasonable:** _TODO — pick a correctly-predicted
row (4 or 5) and explain in a sentence why the label fits the post's content
(e.g. a DD post with short-interest reasoning correctly → `trade_analysis`)._

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
