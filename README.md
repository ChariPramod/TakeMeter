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

<!-- TODO: 2-4 sentences. What does TakeMeter do, for which community, and what
     question does the fine-tuned-vs-baseline comparison answer? -->

_TODO_

---

## Data collection

<!-- TODO: Where the data came from (downloaded public r/wallstreetbets dataset —
     source/link + that you annotated a balanced sample yourself), how you
     annotated it, the final per-class + total counts, AND at least 3 examples
     you found genuinely difficult to label and what you decided.
     (Plan lives in planning.md §6; hardest edge case in §5.) -->

_TODO_

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

<!-- TODO: Base model (distilbert-base-uncased), key hyperparameters
     (epochs, lr, batch size, max length), the seeded stratified 70/15/15 split
     (random_state=42), and that training ran on Colab T4. -->

_TODO_

---

## Evaluation report

<!-- TODO: Compare fine-tuned DistilBERT against the Groq zero-shot baseline.
     Fill in the metrics table and confusion matrix below, then discuss. -->

### Headline metrics

| Model | Accuracy | Macro-F1 | Notes |
|-------|----------|----------|-------|
| Groq zero-shot baseline | _TODO_ | _TODO_ | unparseable: _TODO_ |
| Fine-tuned DistilBERT | _TODO_ | _TODO_ | |

### Confusion matrix (fine-tuned DistilBERT)

<!-- TODO: Replace _TODO_ counts with your actual results.
     Rows = true label, columns = predicted label. -->

| true \ pred | trade_analysis | market_reaction_or_hype | meme_or_shitpost | community_meta_or_news |
|-------------|---------|---------|---------|---------|
| **trade_analysis** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **market_reaction_or_hype** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **meme_or_shitpost** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **community_meta_or_news** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

### Discussion

<!-- TODO: What do the numbers and the matrix show? Which classes get confused,
     and why? Where does the fine-tuned model beat (or lose to) the baseline? -->

_TODO_

---

## Sample classifications

<!-- TODO: A handful of real examples (your collected posts) with the true label,
     the baseline prediction, and the fine-tuned prediction. Include at least one
     where the two models disagree. -->

| Text (excerpt) | True | Baseline | Fine-tuned |
|----------------|------|----------|------------|
| _TODO_ | _TODO_ | _TODO_ | _TODO_ |

---

## Reflection: learned vs. intended

<!-- TODO: Did the model learn what you intended it to, or something correlated
     (length, keywords, surface cues)? Cite evidence (errors, examples,
     confusions) for your conclusion. This is your analysis — write it yourself. -->

_TODO_

---

## Spec reflection

<!-- TODO: Reflect on the project spec / requirements: what was clear, what was
     ambiguous, what you'd change. Your own reflection. -->

_TODO_

---

## AI usage

<!-- TODO: How you used AI tooling and where you kept the work your own.
     The boundary is set in CLAUDE.md and planning.md "AI Tool Plan". -->

AI tooling was used for repo scaffolding and local tooling
(`scripts/validate_dataset.py`, `scripts/baseline_groq.py`). Label design, data
collection, annotation, the baseline system prompt, and all analysis/reflections
are my own work.

_TODO: add specifics._

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
│   ├── reddit_wsb.csv       # the downloaded public WSB dataset (~53k rows)
│   └── dataset.csv          # cleaned + sampled, label BLANK for you to annotate
└── scripts/
    ├── clean_wsb.py         # clean/sample reddit_wsb.csv -> dataset.csv (no labels)
    ├── validate_dataset.py  # pre-Colab dataset sanity check (no GPU)
    └── baseline_groq.py     # local zero-shot Groq baseline (no GPU)
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
