# Zepto AI/ML Engineering Capstone

An end-to-end AI/ML project that combines data engineering, exploratory analysis, predictive modeling, and a retrieval-augmented support assistant in one repository.

The project contains three connected modules:

1. **Data pipeline** — scrapes product data, cleans and enriches it, stores it in normalized SQLite tables, and analyzes it with SQL and pandas.
2. **Analytics** — profiles the Titanic dataset, performs exploratory analysis, trains and evaluates classification and regression models, and saves a complete prediction pipeline.
3. **Support assistant** — builds a Zepto policy question-answering service with local embeddings, ChromaDB, LangGraph, Pydantic, FastAPI, and Docker.

## Repository structure

```text
zepto_capstone_project_aiml/
├── README.md
├── requirements.txt
├── requirements-colab-lock.txt
├── FEATURE_WORKFLOW.md
├── data_pipeline/
│   ├── pipeline.py
│   ├── README.md
│   ├── raw_books.csv
│   ├── clean_books.csv
│   ├── books.db
│   ├── queries.sql
│   └── sql_results.md
├── analytics/
│   ├── pipeline.py
│   ├── README.md
│   ├── titanic.csv
│   ├── results.md
│   ├── interpretations.md
│   ├── model_comparison.csv
│   ├── best_pipeline.joblib
│   └── generated charts
└── support_assistant/
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── Dockerfile
    ├── .dockerignore
    └── docs/
        ├── doc_01.txt
        └── ... doc_08.txt
```

## Setup

### Requirements

- Python 3.11 recommended
- Git
- Internet access for the initial book scrape and first embedding-model download
- Docker Desktop or Docker Engine for container verification

### Install

```bash
git clone https://github.com/sudheermacharla216-lab/zepto_capstone_project_aiml.git
cd zepto_capstone_project_aiml

python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install the consolidated project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 1. Data engineering pipeline

### Objective

The data pipeline collects catalogue data from [Books to Scrape](https://books.toscrape.com/), converts it into analysis-ready fields, and loads it into a normalized relational database.

### Run

From the repository root:

```bash
python data_pipeline/pipeline.py
```

### Workflow

```text
Books to Scrape
      ↓
requests + BeautifulSoup
      ↓
Cleaning and validation
      ↓
GBP-to-INR enrichment
      ↓
Normalized SQLite database
      ↓
SQL queries + pandas validation
```

### Key decisions and results

- Scrapes the first five catalogue pages and visits each product page for category and availability information.
- Produces **100 valid books across 29 categories**, exceeding the minimum requirement of 60 books across three categories.
- Converts price to numeric `price_gbp` values.
- Maps text ratings from One–Five to integers from 1–5.
- Converts availability to the Boolean `in_stock` field.
- Drops and logs rows with unparseable required values rather than inventing price or rating data.
- Calculates `price_inr` using the required fixed project rate:

```text
1 GBP = 105.50 INR
```

- Stores the result in two normalized tables linked by a primary-key/foreign-key relationship:
  - `categories(category_id, category_name)`
  - `books(book_id, title, price_gbp, price_inr, rating, in_stock, category_id)`
- Includes five executed SQL queries covering `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `IN`, `BETWEEN`, and `JOIN`.
- Reproduces the join result with `pandas.merge()` and checks that it matches the SQL output.

See [`data_pipeline/sql_results.md`](data_pipeline/sql_results.md) for the executed queries and results.

## 2. Analytics and machine learning

### Objective

This module uses one consistent Titanic dataset lineage for profiling, cleaning, visualization, classification, imbalance analysis, tuning, regression, and model persistence.

### Run

```bash
python analytics/pipeline.py
```

The committed `analytics/titanic.csv` provides an offline fallback. If it is present, the pipeline reads it instead of downloading the dataset again.

### Data preparation

- Original shape: **891 rows × 15 columns**
- Target balance:
  - Not survived: approximately **61.6%**
  - Survived: approximately **38.4%**
- Missing-value decisions:
  - `embarked` and `embark_town`: about **0.22%** missing; affected rows are dropped under the below-5% rule.
  - `age`: about **19.87%** missing; median imputation is used for EDA and training-only imputation is used for modeling.
  - `deck`: about **77.22%** missing; the column is dropped because reliable imputation is not justified.

### Exploratory analysis

- IQR outliers:
  - Age: **65**
  - Fare: **114**
- Fare is strongly right-skewed:
  - Mean: approximately **32.10**
  - Median: approximately **14.45**
  - Mode: **8.05**
- The six-column correlation matrix contains exactly `survived`, `pclass`, `age`, `sibsp`, `parch`, and `fare`.
- The two strongest absolute off-diagonal correlations are:
  - `pclass` and `fare`: approximately **−0.548**
  - `sibsp` and `parch`: approximately **0.415**
- Four multivariate charts examine survival by sex, passenger class, age, fare, and family size.
- The EDA standardization check confirms that transformed age and fare have approximately zero mean and unit standard deviation.

### Leakage prevention

The train/test split is stratified so both partitions retain the observed class balance. All model preprocessing is contained in scikit-learn pipelines:

- Numeric missing-value imputation
- Categorical missing-value imputation
- One-hot encoding
- Numeric standardization

These steps are fitted only on training data and applied to the test data in transform-only mode.

### Classification results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.815 | 0.797 | 0.691 | 0.740 | **0.861** |
| Decision Tree | 0.809 | 0.815 | 0.647 | 0.721 | 0.856 |
| Random Forest | 0.803 | 0.762 | **0.706** | 0.733 | 0.830 |
| **Tuned Random Forest** | **0.826** | **0.825** | 0.691 | **0.752** | 0.838 |

### Model recommendation

The **tuned Random Forest** is saved as the final complete pipeline because it achieved the strongest training cross-validation F1 score (**0.771**) and the best held-out accuracy (**0.826**) and F1 score (**0.752**). Logistic Regression produced the highest ROC-AUC (**0.861**) and remains a strong option when probability ranking and interpretability are the main priorities. For the project’s F1-based selection rule, the tuned Random Forest is the consistent deployment choice.

The saved artifact includes both preprocessing and the fitted estimator:

```text
analytics/best_pipeline.joblib
```

The pipeline is reloaded and checked on raw, unprocessed test rows to confirm end-to-end prediction.

### Imbalance handling

Logistic Regression was evaluated with three strategies:

| Strategy | CV F1 | Precision | Recall | Test F1 |
|---|---:|---:|---:|---:|
| Baseline | 0.710 | **0.797** | 0.691 | 0.740 |
| Balanced class weights | 0.725 | 0.708 | **0.750** | 0.729 |
| **SMOTE** | **0.731** | 0.746 | 0.735 | **0.741** |

SMOTE achieved the strongest cross-validation F1 and was applied only inside the training pipeline to prevent leakage into the held-out test data.

### Random Forest tuning

`GridSearchCV` tunes `n_estimators`, `max_depth`, and `max_features` with `oob_score=True`.

Best parameters:

```text
max_depth = 8
max_features = 0.8
n_estimators = 100
```

- Best cross-validation F1: approximately **0.771**
- OOB score: approximately **0.819**

### Regression results

A multivariate linear regression predicts fare from the remaining selected features.

| Metric | Value |
|---|---:|
| MAE | 19.646 |
| RMSE | 41.263 |
| R² | 0.347 |
| Adjusted R² | 0.321 |

The residual spread increases substantially in the highest predicted-fare group, providing visual evidence of heteroscedasticity.

Detailed outputs and interpretations are available in:

- [`analytics/results.md`](analytics/results.md)
- [`analytics/interpretations.md`](analytics/interpretations.md)
- [`analytics/model_comparison.csv`](analytics/model_comparison.csv)

## 3. Zepto policy support assistant

### Objective

The support assistant answers questions grounded in eight supplied Zepto policy documents. Its graded default mode is deterministic and requires no LLM API key.

### Architecture

```text
Eight policy documents
        ↓
Document ingestion and chunking
        ↓
all-MiniLM-L6-v2 embeddings
        ↓
ChromaDB cosine-similarity index
        ↓
LangGraph intent classifier
       / \
      /   \
Policy     General
query      query
  ↓          ↓
Top-3       Fixed direct
retrieval   response
  ↓          ↓
Validated Pydantic response
        ↓
FastAPI POST /ask
```

### Components

- **Ingestion:** `resources()` loads all eight `docs/doc_*.txt` files, using one short policy document per chunk.
- **Embedding:** `SentenceTransformer` uses `all-MiniLM-L6-v2` locally.
- **Storage:** ChromaDB stores the vectors in the `zepto_policies` collection with cosine distance.
- **Routing:** a LangGraph `StateGraph` uses the nodes `classify_intent`, `retrieve_and_answer`, and `direct_answer`.
- **Retrieval:** policy queries retrieve the three closest policy documents.
- **Generation:** mock mode returns a deterministic excerpt from the best retrieved document. The optional real-LLM path uses a structured role–context–task–format–length prompt.
- **Validation:** Pydantic enforces the response fields `answer`, `sources`, and `confidence`.
- **API:** FastAPI exposes the graph through `POST /ask`.

### MOCK_LLM behavior

`MOCK_LLM` defaults to `1`, which is the required offline baseline:

- No LLM provider is contacted.
- Intent classification uses the required keyword heuristic.
- Policy questions use real local embedding and ChromaDB retrieval.
- Policy responses start with `Based on the retrieved context:`.
- General questions receive a fixed response.

When `MOCK_LLM=0`, the optional real-LLM path calls the configured endpoint, validates its JSON response, and retries up to two additional times after validation failure.

### Run locally

Linux or macOS:

```bash
MOCK_LLM=1 uvicorn main:app --app-dir support_assistant --host 0.0.0.0 --port 7860
```

Windows PowerShell:

```powershell
$env:MOCK_LLM="1"
uvicorn main:app --app-dir support_assistant --host 0.0.0.0 --port 7860
```

Open the interactive API documentation at:

```text
http://127.0.0.1:7860/docs
```

### Example policy request

```bash
curl -X POST http://127.0.0.1:7860/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the refund policy for damaged grocery items?"}'
```

Example response:

```json
{
  "answer": "Based on the retrieved context: Returns & Refunds...",
  "sources": ["doc_02", "doc_06", "doc_05"],
  "confidence": 1.0
}
```

### Example general request

```bash
curl -X POST http://127.0.0.1:7860/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"What is two plus two?"}'
```

Example response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

## Docker

Build the support-assistant image from the repository root:

```bash
docker build -t zepto-support support_assistant
```

Run the container in default mock mode:

```bash
docker run --rm -p 7860:7860 -e MOCK_LLM=1 zepto-support
```

The container serves the endpoint at `http://localhost:7860/ask`.

### Recorded verification

- Docker image build: passed
- Docker container startup: passed
- FastAPI service on port 7860: passed
- Policy request: HTTP 200 with the expected retrieved sources
- General request: HTTP 200 with an empty source list
- Pydantic response validation: passed
- Default mock mode: passed without an LLM API call

## Git workflow

The repository history demonstrates the required workflow:

1. The `feature/final-capstone-review` branch was created.
2. Two commits were made on the feature branch.
3. The feature branch was merged into `main` with a merge commit.

This history can be inspected with:

```bash
git log --graph --all --oneline
```

## Reproducibility and limitations

- The GBP-to-INR rate is an assignment-defined constant and is not a live exchange rate.
- The Titanic dataset is historical and is used only for educational analysis. The resulting model is not validated for real customer or operational decisions.
- Mock confidence values are deterministic schema values rather than calibrated probabilities.
- The supplied policy files are the assistant’s only source of policy evidence and should not be interpreted as confirmation of Zepto’s current public policies.
- The optional real-LLM path requires user-provided endpoint settings. No API key is stored in this repository.

## Technologies

- Python
- pandas and NumPy
- requests and BeautifulSoup
- SQLite
- Matplotlib and Seaborn
- scikit-learn and imbalanced-learn
- Sentence Transformers
- ChromaDB
- LangGraph
- Pydantic
- FastAPI and Uvicorn
- Docker

## Submission repository

[https://github.com/sudheermacharla216-lab/zepto_capstone_project_aiml](https://github.com/sudheermacharla216-lab/zepto_capstone_project_aiml)
