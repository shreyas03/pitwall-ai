# Pitwall AI
[![CI Pipeline](https://github.com/shreyas03/pitwall-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/shreyas03/pitwall-ai/actions/workflows/ci.yml)
A multi-agent system that answers Formula 1 questions by writing and running real Python code against a local SQLite database, instead of generating answers from a model's memory. Built with Microsoft's AutoGen (ag2) framework and GPT-4o-mini.

## The problem it solves

Ask an LLM a specific stat — "who won the 2015 Belgian Grand Prix?" — and it will often answer fluently and get it wrong. Pitwall AI avoids that by never letting the model state a number it hasn't just computed. Every answer is grounded in the printed output of a script the model wrote and an agent actually executed against the real F1 database.

## Architecture

Two AutoGen agents talk to each other:

- **Race Engineer** — the reasoning agent. Given a question, it writes a Python script (using `sqlite3` and `pandas`) that queries `Formula1.sqlite`, inspecting the schema first if needed. It does not answer directly; it writes code to find the answer.
- **Team Principal** — the execution agent (played by you, the user, via AutoGen's human-input mode). It runs the Race Engineer's code locally and returns the terminal output. Only after seeing real output does the Race Engineer explain the answer in plain text and end the conversation.

Write the code, run it, read the actual output, then answer. That loop is what eliminates hallucination — the model can't skip straight to a confident-sounding number; it has to derive it from a query it just ran.

## Data

`Formula1.sqlite` is a local copy of the Ergast F1 database (races, results, drivers, constructors, lap times, pit stops, standings — seasons 1950–2017).

`f1_data_fetcher.py` is a separate utility for pulling finalized driver/constructor standings for a given season directly from the [Ergast API mirror](https://api.jolpi.ca/ergast/f1), for cases where you want current data outside the local snapshot.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# then add your OpenAI API key to .env
```

## Run

```bash
python pitwall.py
```

You'll be prompted for a question. The Race Engineer will write and propose a script; you (as Team Principal) approve execution, and the terminal output gets fed back into the conversation for the final answer.

## Testing & CI/CD

The repository includes an automated test suite executed via **GitHub Actions** across Python 3.11 and 3.12:

- **Unit Testing (`pytest`):** Validates local SQLite schema integrity and leverages `unittest.mock` to test Ergast API response parsing, pandas DataFrame normalization, and network exception handling without live HTTP dependencies.
- **Static Analysis (`ruff`):** Automatically checks code formatting, syntax integrity, and unused imports on every pull request and push to `main`.

Run tests locally:
```bash
python -m pytest tests/ -v
```

## Repo contents

- `pitwall.py` — agent definitions and the AutoGen conversation loop
- `f1_data_fetcher.py` — standalone helper for fetching live standings from the Ergast API
- `Formula1.sqlite` — local F1 database (1950–2017)
- `tests/` — automated unit and mocked API test suites
- `.github/workflows/ci.yml` — automated CI/CD pipeline definition
- `requirements.txt`
- `.env.example` — template for the required `OPENAI_API_KEY`