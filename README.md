# Zepto AI/ML capstone

One repository with data_pipeline, analytics, and support_assistant. This is an educational assignment using a books catalogue, Titanic, and a supplied policy corpus. The modules share the platform narrative and repository; Titanic is not presented as real Zepto customer data.

## Setup
Use Python 3.11 or a compatible Colab runtime. Install the **consolidated root requirements.txt**: `python -m pip install -r requirements.txt`. requirements-colab-lock.txt records the environment used to run this notebook, when exported. support_assistant/requirements.txt is a smaller standalone dependency list for its Docker image. First-run downloads and scraping need internet.

## Run from the repository root
1. `python data_pipeline/pipeline.py` — scrape, clean, convert, create SQLite and save SQL/pandas results.
2. `python analytics/pipeline.py` — reuse titanic.csv if present, then EDA, classifier comparisons, balancing, tuning, regression and saved full pipeline. The first execution uses Seaborn once and saves titanic.csv immediately.
3. `MOCK_LLM=1 uvicorn main:app --app-dir support_assistant --host 0.0.0.0 --port 7860` — use POST /ask as documented in support_assistant/README.md. On Windows PowerShell set `$env:MOCK_LLM="1"` first, then run the uvicorn command without the prefix.
4. Run Docker build/run and both curl examples in support_assistant/README.md on a Docker-capable machine.

## Design decisions and results
Data pipeline: first five catalogue pages plus detail-page categories; malformed fields are dropped/logged, with minimum-size checks. Fixed artificial rate: **1 GBP = 105.50 INR**. Two tables enforce category PK/FK normalization. Read data_pipeline/README.md and sql_results.md.

Analytics: one dataset lineage, percentage-based EDA decisions, identical model split, train-only preprocessing pipelines, CV-only classifier selection, training-only SMOTE, RF OOB reporting and full-pipeline persistence. EDA-imputed values are not passed to models. Read analytics/results.md and my completed analytics/interpretations.md.

Assistant: per-document chunks, local MiniLM embeddings, cosine Chroma retrieval, three LangGraph nodes, validated FastAPI JSON, mock default and an optional real-generation branch with retries. Read support_assistant/README.md for the detailed architecture and actual API transcripts.

## Submission
Include code, required Markdown explanations, titanic.csv, SQL outputs and reproducible scripts. Plots are supporting artifacts. Do not commit credentials or local model/cache folders. Save your executed Colab notebook into this repository too. Create a real feature branch, make at least two meaningful commits there as you work, and merge it with a merge commit into main. Submit exactly one public repository URL.

## Verification status
The notebook has been executed through the project pipeline and the generated artifacts, machine-learning models, retrieval pipeline and FastAPI MOCK_LLM endpoint have been checked. Docker configuration is included; the Docker image should also be built and run on a Docker-capable machine before final submission.
