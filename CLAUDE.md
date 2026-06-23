# CLAUDE.md — Project rules for AI sessions

This file captures the non-negotiable rules for working on **TakeMeter**
(CodePath AI201 Project 3). Future sessions must respect these.

## What this project is

A fine-tuned **DistilBERT** classifier that scores **discourse quality** in an
online community, compared against a zero-shot **Groq `llama-3.3-70b-versatile`**
baseline.

## HARD RULE — no fabrication, no doing the student's intellectual work

Do **not**, under any circumstances:
- invent or suggest specific **labels** / a label taxonomy
- **fabricate, generate, or scrape** posts or any dataset rows
- write the **analysis, evaluation writeup, or reflections**
- write the baseline **system prompt** (the classification instructions)

Label design, data collection, annotation, the system prompt, and all
writeups/reflections are **the student's own work**. Wherever a decision belongs
to the student, leave a clearly marked `TODO` placeholder — never a guess
presented as an answer.

Your role is **scaffolding, tooling, and validation** only.

## GPU / Colab constraint

Fine-tuning runs on **Google Colab (free T4 GPU)** using the provided starter
notebook — **NOT locally**. This repo holds everything *outside* the notebook,
plus local (no-GPU) tooling to de-risk Colab runs:
- `scripts/validate_dataset.py` — pre-upload dataset sanity check
- `scripts/baseline_groq.py` — local zero-shot Groq baseline (API call, no GPU)

Do not add local GPU/training code or try to run fine-tuning here. Keep heavy
ML deps (torch, transformers, datasets) in the notebook, not in
`requirements-local.txt`.

## Consistency requirements

- The split must stay **stratified 70/15/15 with `random_state=42`** so the
  local baseline matches what Colab would produce.
- Label strings must stay consistent across `data/`, `scripts/validate_dataset.py`
  (`LABEL_MAP`), the notebook, and `README.md`.
- The baseline output parsing (substring match, longest-label-first) must match
  the notebook's parsing.

## Conventions

- Secrets live in `.env` (gitignored); see `.env.example`.
- Student decisions are marked with `TODO` in code and docs.
