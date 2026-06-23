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

<!-- TODO: Where the data came from (r/anime — link + collection method), how you
     collected and annotated it, the final per-class + total counts, AND at least
     3 examples you found genuinely difficult to label and what you decided.
     (Plan lives in planning.md §4; hardest edge case in §3.) -->

_TODO_

---

## Label taxonomy

Community: **r/anime**. Three labels (see [planning.md](planning.md) §2 for full
definitions, examples, and the edge-case decision rule). These must match
`LABEL_MAP` in [scripts/validate_dataset.py](scripts/validate_dataset.py) and the
Colab notebook.

| Label | Definition (short — see [planning.md](planning.md) §2 for full) |
|-------|------------|
| `help_request` | Primarily asks the community for a recommendation, ID, watch-order, or streaming/access answer — expected replies are practical suggestions or facts. |
| `reaction_or_event` | Primarily reacts to or organizes discussion around a specific episode, trailer, visual, announcement, rewatch, or event — immediate impressions/hype over developed argument. |
| `substantive_discussion` | Primarily develops or invites an opinion, critique, comparison, or interpretation that requires reasoning about anime, production, or fandom. |

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

<!-- TODO: Replace placeholder labels/values with your actual results.
     Rows = true label, columns = predicted label. -->

| true \ pred | class_a | class_b | class_c |
|-------------|---------|---------|---------|
| **class_a** | _TODO_  | _TODO_  | _TODO_  |
| **class_b** | _TODO_  | _TODO_  | _TODO_  |
| **class_c** | _TODO_  | _TODO_  | _TODO_  |

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
├── planning.md              # required planning sections (your work)
├── README.md                # this file
├── CLAUDE.md                # project rules for AI sessions
├── requirements-local.txt   # deps for local tooling (no GPU)
├── .env.example             # copy to .env, add API keys
├── data/
│   ├── dataset_template.csv # column template: text,label,notes
│   └── dataset.csv          # collected (API) + annotated (you) data
└── scripts/
    ├── collect_reddit.py    # fetch PUBLIC r/anime text via official Reddit API
    ├── validate_dataset.py  # pre-Colab dataset sanity check (no GPU)
    └── baseline_groq.py     # local zero-shot Groq baseline (no GPU)
```

## Local setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-local.txt
cp .env.example .env        # then add GROQ_API_KEY + REDDIT_* credentials
```

### 1. Collect text (official Reddit API — not scraping)

Uses Reddit's sanctioned API to fetch **public** r/anime posts/comments into
`data/dataset.csv` with the `label` column left blank. Create a free "script"
app at <https://www.reddit.com/prefs/apps>, put the credentials in `.env`, then:

```bash
python scripts/collect_reddit.py --submissions --comments --per-source 80
```

Fetching only retrieves text + permalinks; it does **not** label anything.
Annotation is your work and stays within Reddit's API terms of use.

### 2. Annotate, validate, baseline

```bash
# Open data/dataset.csv and fill the `label` column with one of your 3 labels
# (planning.md §2). Then validate before uploading to Colab:
python scripts/validate_dataset.py data/dataset.csv

# Run the zero-shot baseline locally (after filling in SYSTEM_PROMPT):
python scripts/baseline_groq.py data/dataset.csv
```
