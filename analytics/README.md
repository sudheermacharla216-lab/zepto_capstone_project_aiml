# Analytics
Install root requirements; run `python analytics/pipeline.py` from the repository root.
The first run loads Titanic with Seaborn and immediately saves titanic.csv. Later runs reuse that CSV, including offline grading. The same retained cohort supplies EDA and modeling; EDA-imputed values are not fed to models. Training-only pipeline imputers preserve the evaluation boundary. alive and redundant derived flags are excluded from model inputs.

results.md contains measured results and writing prompts. interpretations.md must contain your own completed interpretations for the four story charts, correlations, skewness, imbalance, residuals and final recommendation. best_pipeline.joblib includes preprocessing and classifier and is checked on raw inputs after reloading.

Model choice uses training CV F1; the tuned forest's maximum CV score can be optimistic from hyperparameter selection. The held-out test results provide a separate estimate. OOB is supplementary because preprocessing is fitted on the full training split. SMOTE after one-hot encoding can produce fractional indicators; this limitation is disclosed.
