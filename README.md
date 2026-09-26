# Zepto Data & AI Platform

## Capstone Project — Artificial Intelligence & Machine Learning

The **Zepto Data & AI Platform** is an end-to-end AI/ML capstone project demonstrating data engineering, exploratory data analysis, machine learning, retrieval-augmented generation (RAG), LangGraph orchestration, FastAPI, and Docker deployment.

The project is organized as one integrated repository containing three modules:

1. **Data Engineering Pipeline**
2. **Analytics & Machine Learning Pipeline**
3. **GenAI Support Assistant**

The complete workflow demonstrates how raw data can be collected, cleaned, stored, analyzed, modeled, and finally used by an AI-powered support application.

---

# Project Architecture

```text
zepto_capstone/
│
├── README.md
├── requirements.txt
│
├── data_pipeline/
│   ├── pipeline.py
│   ├── books.db
│   ├── sql_results.md
│   └── README.md
│
├── analytics/
│   ├── pipeline.py
│   ├── titanic.csv
│   ├── results.md
│   ├── interpretations.md
│   ├── model_comparison.csv
│   └── best_pipeline.joblib
│
└── support_assistant/
    ├── main.py
    ├── Dockerfile
    ├── README.md
    └── docs/
        ├── doc_01.txt
        ├── doc_02.txt
        ├── doc_03.txt
        ├── doc_04.txt
        ├── doc_05.txt
        ├── doc_06.txt
        ├── doc_07.txt
        └── doc_08.txt
```

---

# Technology Stack

The project uses:

- Python
- Pandas
- NumPy
- Requests
- BeautifulSoup
- SQLite
- Matplotlib
- Seaborn
- Scikit-learn
- Imbalanced-learn / SMOTE
- Joblib
- Sentence Transformers
- ChromaDB
- LangGraph
- Pydantic
- FastAPI
- Uvicorn
- Docker
- Git
- GitHub

---

# Installation

Clone the repository:

```bash
git clone https://github.com/sudheermacharla216-lab/zepto_capstone_project_aiml.git
cd zepto_capstone_project_aiml
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

This project uses a consolidated root `requirements.txt` for the required Python dependencies.

---

# Module 1 — Data Engineering Pipeline

## Objective

The first module demonstrates a complete data-engineering workflow:

```text
Web Scraping
     ↓
Raw Product Data
     ↓
Data Cleaning
     ↓
Currency Conversion
     ↓
Normalized SQLite Database
     ↓
SQL Analysis
     ↓
Pandas Analysis
```

The source is **Books to Scrape**, a public website designed for web-scraping practice.

---

## Web Scraping

The pipeline uses:

- `requests`
- `BeautifulSoup`

The scraper collects at least **60 books across at least three categories**.

The following information is captured:

- title
- price in GBP
- star rating
- availability
- category

---

# Data Cleaning

The scraped values are converted into appropriate data types.

### Price

The GBP currency symbol is removed and the value is converted to `float`.

```text
price_gbp → float
```

### Rating

Text ratings are converted to integer values:

```text
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5
```

### Availability

Availability is converted into a Boolean representation:

```text
In stock     → True
Out of stock → False
```

Unexpected or invalid values are handled so that malformed rows do not cause the complete pipeline to fail.

---

# GBP to INR Conversion

The assignment-defined fixed exchange rate is used:

```text
1 GBP = 105.50 INR
```

The converted price is calculated as:

```python
price_inr = price_gbp * 105.50
```

This is a fixed project baseline and does not depend on a live exchange-rate API.

---

# SQLite Database

The cleaned data is stored in a normalized SQLite database.

Database:

```text
data_pipeline/books.db
```

The schema contains two related tables.

## Categories

```text
categories
----------
category_id INTEGER PRIMARY KEY
category_name TEXT UNIQUE
```

## Books

```text
books
-----
book_id INTEGER PRIMARY KEY
title TEXT
price_gbp REAL
price_inr REAL
rating INTEGER
in_stock INTEGER
category_id INTEGER
```

`category_id` is used as the foreign-key relationship between books and categories.

---

# SQL Analysis

The project executes at least five SQL queries demonstrating the required SQL operations, including:

- SELECT
- WHERE
- ORDER BY
- LIMIT
- DISTINCT
- IN / BETWEEN
- JOIN

The SQL results are recorded in:

```text
data_pipeline/sql_results.md
```

The project also demonstrates:

```python
pd.read_sql()
```

for loading SQL results into Pandas DataFrames.

The SQL JOIN result is additionally reproduced using:

```python
pd.merge()
```

to demonstrate equivalent relational operations in Pandas.

---

# Running Module 1

From the repository root:

```bash
python data_pipeline/pipeline.py
```

The pipeline performs the scraping, cleaning, conversion, database creation, SQL analysis, and Pandas comparison workflow.

---

# Module 2 — Analytics & Machine Learning

## Objective

The second module demonstrates an end-to-end data-science workflow using the Titanic dataset.

The workflow is:

```text
Titanic Dataset
      ↓
Data Profiling
      ↓
Missing-Value Analysis
      ↓
EDA
      ↓
Feature Processing
      ↓
Train/Test Split
      ↓
Machine Learning
      ↓
Evaluation
      ↓
Hyperparameter Tuning
      ↓
Saved ML Pipeline
```

A committed copy of the dataset is available at:

```text
analytics/titanic.csv
```

This acts as the offline fallback so the project does not depend on network availability during evaluation.

---

# Data Profiling

The dataset is inspected using:

```python
df.info()
df.describe()
df.shape
```

Missing-value percentages are calculated for affected columns before selecting the appropriate handling strategy.

The assignment threshold rules are applied:

```text
< 5% missing     → drop affected rows where appropriate
5%–30% missing   → imputation
Very high missing → drop column or explicitly encode missingness
```

The decisions and interpretations are documented in the analytics results/interpretation files.

---

# Exploratory Data Analysis

## Univariate Analysis

`age` and `fare` are analyzed using:

- Histograms
- Box plots
- Descriptive statistics
- IQR outlier detection

Observed IQR outlier counts:

```text
Age  : 65
Fare : 114
```

Fare statistics:

```text
Mean   ≈ 32.10
Median ≈ 14.45
Mode   ≈ 8.05
```

Because the mean is substantially greater than the median and mode, the fare distribution is strongly right-skewed.

---

# Bivariate Analysis

Survival behavior is analyzed by:

- sex
- passenger class
- sex + passenger class

Boolean masking is used for the required grouped analysis.

---

# Correlation Analysis

The correlation matrix uses exactly:

```text
survived
pclass
age
sibsp
parch
fare
```

Derived Boolean columns such as `adult_male` and `alone` are excluded.

Among the strongest observed relationships were:

```text
pclass vs fare ≈ -0.548
sibsp vs parch ≈ 0.415
```

The first relationship indicates that passenger class and fare are strongly associated, while the second reflects the relationship between sibling/spouse and parent/child family counts.

---

# Multivariate Analysis

Multiple visualizations are used to build a survival data story.

The analysis examines relationships involving:

- sex
- passenger class
- age
- fare
- survival

Each required visualization is accompanied by written interpretation.

---

# Standardization

The exploratory analysis demonstrates z-score standardization for:

```text
age
fare
```

using:

```text
z = (x - mean) / standard deviation
```

The transformed variables are checked to confirm an approximately zero mean and unit standard deviation.

This EDA transformation is separate from the preprocessing used by the predictive-modeling pipeline.

---

# Train/Test Split

The classification dataset is split before model preprocessing.

A **stratified train/test split** is used to preserve the survival-class distribution in both training and test data.

All model preprocessing is fit only on training data to prevent information leakage.

---

# Preprocessing Pipeline

The modeling workflow uses Scikit-learn pipeline components such as:

```text
ColumnTransformer
       ↓
Imputation
       ↓
Categorical Encoding
       ↓
StandardScaler
       ↓
Classifier
```

Categorical features such as:

```text
sex
embarked
```

are encoded.

Numerical features are scaled using:

```python
StandardScaler
```

Preprocessing is learned only from the training data and then applied to the test set.

---

# Classification Models

Three classifiers are trained on the same train/test split:

### Logistic Regression

Test results:

```text
Accuracy  ≈ 0.815
Precision ≈ 0.797
Recall    ≈ 0.691
F1        ≈ 0.740
AUC       ≈ 0.861
```

### Decision Tree

```text
Accuracy  ≈ 0.809
Precision ≈ 0.815
Recall    ≈ 0.647
F1        ≈ 0.721
AUC       ≈ 0.856
```

### Random Forest

```text
Accuracy  ≈ 0.803
Precision ≈ 0.762
Recall    ≈ 0.706
F1        ≈ 0.733
AUC       ≈ 0.830
```

The Decision Tree is additionally visualized using `plot_tree`.

---

# Model Evaluation

The classifiers are evaluated using:

- Confusion Matrix
- Accuracy
- Precision
- Recall
- F1 Score
- ROC Curve
- AUC

The comparison results are saved in:

```text
analytics/model_comparison.csv
```

---

# Class Imbalance Handling

Three approaches are compared:

### Baseline

```text
Precision ≈ 0.797
Recall    ≈ 0.691
F1        ≈ 0.740
```

### Class Weight Balanced

```text
Precision ≈ 0.708
Recall    ≈ 0.750
F1        ≈ 0.729
```

### SMOTE

```text
Precision ≈ 0.746
Recall    ≈ 0.735
F1        ≈ 0.741
```

SMOTE is applied only to training data/folds so that information from the test set does not leak into model training.

The comparison illustrates the trade-off between precision and recall when different imbalance-handling strategies are used.

---

# Random Forest Hyperparameter Tuning

`GridSearchCV` is used to tune:

```text
n_estimators
max_depth
max_features
```

The Random Forest is constructed with:

```python
oob_score=True
```

so its out-of-bag score can also be evaluated.

The best cross-validation F1 score observed during tuning was approximately:

```text
0.771
```

with an OOB score of approximately:

```text
0.819
```

---

# Regression Task

A multivariate Linear Regression model is used to predict passenger fare.

Evaluation results:

```text
MAE          ≈ 19.65
RMSE         ≈ 41.26
R²           ≈ 0.347
Adjusted R²  ≈ 0.321
```

A residual plot is used to examine whether prediction errors show a non-random change in variance and to discuss heteroscedasticity.

---

# Final Model Selection

For the classification task, Logistic Regression provides a strong overall result on the evaluated split, including approximately:

```text
Accuracy = 0.815
F1       = 0.740
AUC      = 0.861
```

These results are considered together with the Decision Tree, Random Forest, and imbalance-handling experiments when documenting the deployment choice.

Classification and regression metrics are kept separate because they measure different types of predictive tasks and are not directly comparable on a common scale.

---

# Saved Machine Learning Pipeline

The final fitted pipeline is saved as:

```text
analytics/best_pipeline.joblib
```

The artifact contains both:

```text
Preprocessing
+
Final estimator
```

rather than only the estimator.

It can therefore accept raw input and apply the same preprocessing learned during training.

The project also reloads the saved pipeline using:

```python
joblib.load()
```

and verifies that prediction still works.

---

# Running Module 2

Run:

```bash
python analytics/pipeline.py
```

The module performs the analytics and machine-learning workflow and generates the required evaluation outputs.

---

# Module 3 — GenAI Support Assistant

## Objective

The third module builds a policy-focused Retrieval-Augmented Generation system.

Architecture:

```text
User Question
      ↓
FastAPI
      ↓
LangGraph
      ↓
Intent Classification
      ↓
 ┌────────────────────┐
 │                    │
Policy Question    General Question
 │                    │
 ↓                    ↓
Retrieval          Direct Answer
 │
 ↓
ChromaDB
 │
 ↓
Top-3 Chunks
 │
 ↓
Grounded Answer
 │
 └───────────┬────────
             ↓
      Pydantic Validation
             ↓
        JSON Response
```

---

# Policy Corpus

The project contains eight Zepto policy documents:

```text
doc_01 — Delivery Policy
doc_02 — Returns & Refunds
doc_03 — Membership Tiers
doc_04 — Order Tracking
doc_05 — Order Cancellation Policy
doc_06 — Damaged or Missing Items
doc_07 — Gift Cards
doc_08 — Customer Support Hours
```

These documents form the knowledge base for the support assistant.

---

# RAG Pipeline Architecture

The RAG pipeline contains four main stages.

## 1. Ingestion

The eight policy documents in:

```text
support_assistant/docs/
```

are loaded by the support-assistant application.

Each document is converted into a chunk suitable for embedding and retrieval.

## 2. Embedding

Embeddings are generated locally using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

No paid embedding API is required.

## 3. Retrieval

The document embeddings are stored in:

```text
ChromaDB
```

For a policy question, the query is embedded and compared with the stored policy vectors.

The system retrieves the:

```text
Top 3
```

most similar chunks using cosine-based similarity.

## 4. Generation

The retrieved context is passed to the answer-generation stage.

In the required default mock mode, the response is generated deterministically from the top retrieved context.

The optional real-LLM path can use the structured prompt while remaining grounded in the retrieved context.

---

# LangGraph Workflow

The application uses a LangGraph `StateGraph` with a typed state.

The three primary nodes are:

```text
classify_intent
retrieve_and_answer
direct_answer
```

The routing architecture is:

```text
                  classify_intent
                         |
              ┌──────────┴──────────┐
              │                     │
       policy_question       general_question
              │                     │
              ↓                     ↓
   retrieve_and_answer         direct_answer
              │                     │
              └──────────┬──────────┘
                         ↓
                        END
```

---

# Intent Classification

In default mock mode, classification is deterministic.

Policy keywords include:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

Questions containing policy-related keywords are routed to:

```text
retrieve_and_answer
```

Other questions are routed to:

```text
direct_answer
```

---

# MOCK_LLM Mode

The required graded baseline uses:

```text
MOCK_LLM=1
```

or leaves the environment variable unset.

This mode requires no external LLM API key.

For policy questions:

```text
Query
 ↓
Retrieve top-3 policy chunks
 ↓
Use top retrieved context
 ↓
Return deterministic grounded response
```

The mock response follows the required pattern:

```text
Based on the retrieved context: ...
```

For unrelated questions, the application returns:

```text
I can only answer questions about Zepto policies right now.
```

---

# Structured Prompt

The optional real-LLM path uses a structured prompt following:

```text
Role
Context
Task
Format
Length
```

The prompt includes an explicit grounding constraint instructing the model not to answer from information outside the supplied policy context.

It also includes a few-shot example showing the expected question-and-answer behavior.

---

# Structured Output

Responses are validated using a Pydantic response model.

Example:

```json
{
  "answer": "Response text",
  "sources": ["doc_02", "doc_06"],
  "confidence": 1.0
}
```

The schema contains:

```text
answer     → string
sources    → list of source IDs
confidence → float between 0 and 1
```

---

# FastAPI

The LangGraph application is exposed through FastAPI.

Endpoint:

```text
POST /ask
```

Request schema:

```json
{
  "query": "What is the refund policy?"
}
```

---

# Example — Policy Question

Request:

```json
{
  "query": "What is the refund policy?"
}
```

Example verified response:

```json
{
  "answer": "Based on the retrieved context: Returns & Refunds ...",
  "sources": [
    "doc_02",
    "doc_06",
    "doc_05"
  ],
  "confidence": 1.0
}
```

This request triggers:

```text
classify_intent
      ↓
policy_question
      ↓
retrieve_and_answer
      ↓
ChromaDB Top-3 Retrieval
```

---

# Example — General Question

Request:

```json
{
  "query": "What is two plus two?"
}
```

Verified response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

This request follows:

```text
classify_intent
      ↓
general_question
      ↓
direct_answer
```

No policy retrieval is required.

---

# Running the Support Assistant Locally

Move into the module:

```bash
cd support_assistant
```

Enable mock mode.

### Windows PowerShell

```powershell
$env:MOCK_LLM="1"
```

### Linux / macOS

```bash
export MOCK_LLM=1
```

Start FastAPI:

```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

Then open:

```text
http://localhost:7860/docs
```

Swagger UI can be used to test the `/ask` endpoint.

---

# Docker

The support assistant contains a Dockerfile for reproducible local deployment.

## Build

From the repository root:

```bash
docker build -t zepto-support support_assistant
```

## Run

```bash
docker run --rm -p 7860:7860 -e MOCK_LLM=1 zepto-support
```

Then access:

```text
http://localhost:7860/docs
```

---

# Docker Verification

The Docker implementation was tested locally using Docker Desktop.

Verification status:

```text
Dockerfile              : VERIFIED
Docker image build      : PASSED
Docker container run    : PASSED
FastAPI /ask            : PASSED
Policy retrieval route  : PASSED
General query route     : PASSED
Structured output       : PASSED
MOCK_LLM mode           : PASSED
```

The Docker image:

```text
zepto-support:latest
```

built successfully.

The container successfully served FastAPI on:

```text
localhost:7860
```

Both the policy-query route and general-query route returned HTTP 200 responses during verification.

---

# Git Workflow

The project follows the required feature-branch workflow.

Development included:

```text
main
  │
  ├── feature/final-capstone-review
  │       │
  │       ├── Commit 1
  │       └── Commit 2
  │
  └──── Merge into main
```

The repository history therefore demonstrates:

- Feature branch creation
- At least two commits on the feature branch
- Merge back into `main`

The workflow can be inspected using:

```bash
git log --graph --oneline --decorate --all
```

---

# Design Decisions

## Data Engineering

A normalized two-table SQLite design was chosen to separate book data from category data and demonstrate primary-key/foreign-key relationships.

The fixed assignment conversion rate of:

```text
1 GBP = 105.50 INR
```

is used rather than depending on an external exchange-rate API.

## Machine Learning

Scikit-learn pipelines and `ColumnTransformer` are used so preprocessing and modeling remain part of a reproducible workflow.

The train/test split is performed before fitting preprocessing steps to prevent data leakage.

Stratification is used because survival is a binary classification target with unequal class frequencies.

## GenAI / RAG

Local sentence-transformer embeddings and ChromaDB were selected so retrieval can operate without paid APIs.

LangGraph provides explicit routing between policy and general questions.

`MOCK_LLM=1` provides deterministic offline behavior and is the primary project baseline.

Pydantic guarantees a consistent API response structure.

## Deployment

FastAPI provides a lightweight REST interface.

Docker packages the application and its dependencies into a reproducible local environment.

---

# Reproducibility

The project is designed to remain reproducible without paid services.

The main offline/reproducibility features include:

- Fixed GBP-to-INR project conversion rate
- Committed SQLite output/recreation pipeline
- Committed Titanic CSV fallback
- Saved fitted ML pipeline
- Local SentenceTransformer embeddings
- Local ChromaDB vector storage
- Deterministic MOCK_LLM mode
- Dockerized FastAPI application

---

# Main Deliverables

```text
README.md
requirements.txt

data_pipeline/
    pipeline.py
    books.db
    sql_results.md

analytics/
    pipeline.py
    titanic.csv
    results.md
    interpretations.md
    model_comparison.csv
    best_pipeline.joblib

support_assistant/
    main.py
    Dockerfile
    README.md
    docs/
        doc_01.txt
        doc_02.txt
        doc_03.txt
        doc_04.txt
        doc_05.txt
        doc_06.txt
        doc_07.txt
        doc_08.txt
```

---

# Project Summary

This capstone demonstrates a complete AI/ML engineering workflow:

```text
DATA ENGINEERING
Web Scraping
      ↓
Cleaning
      ↓
SQLite
      ↓
SQL + Pandas

DATA SCIENCE
Titanic
      ↓
EDA
      ↓
Preprocessing
      ↓
Machine Learning
      ↓
Evaluation + Tuning
      ↓
Saved Pipeline

GENERATIVE AI
Policy Documents
      ↓
SentenceTransformer
      ↓
ChromaDB
      ↓
LangGraph
      ↓
RAG
      ↓
Pydantic
      ↓
FastAPI
      ↓
Docker
```

Together, the three modules demonstrate practical skills across data engineering, data analysis, machine learning, GenAI/RAG, API development, containerization, and Git-based software-development workflows.

---

# Repository

GitHub Repository:

https://github.com/sudheermacharla216-lab/zepto_capstone_project_aiml

---

# Author

**Sudheer Kumar**

AI/ML Capstone Project

---

# Project Status

**COMPLETED**

- Data Engineering Pipeline — Complete
- Analytics & Machine Learning Pipeline — Complete
- GenAI/RAG Support Assistant — Complete
- FastAPI — Verified
- Docker — Verified
- Git workflow — Complete
- GitHub repository — Complete
