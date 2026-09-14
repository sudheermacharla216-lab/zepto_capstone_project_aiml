from pathlib import Path
import io, json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
AN = Path('analytics')
AN.mkdir(exist_ok=True)
fallback = AN / 'titanic.csv'
if fallback.exists():
    raw = pd.read_csv(fallback)
else:
    raw = sns.load_dataset('titanic')
    raw.to_csv(fallback, index=False)
raw.info()
print(raw.describe().to_string())
print('Shape:', raw.shape)
missing = raw.isna().mean().mul(100)
missing = missing[missing.gt(0)].sort_values(ascending=False)
print('Missing percentages:\n', missing.to_string())
print('Target balance:\n', raw.survived.value_counts(normalize=True).to_string())
buf = io.StringIO()
raw.info(buf=buf)
notes = ['# Analytics results', '## Profile', '```text\n'+buf.getvalue()+'\n```',
         raw.describe().to_markdown(), f'Shape: {raw.shape}',
         missing.rename('missing_percent').to_frame().to_markdown(),
         raw.survived.value_counts(normalize=True).rename('fraction').to_frame().to_markdown()]
def add_note(title, text):
    notes.extend(['## '+title, str(text)])
def save_plot(name):
    plt.tight_layout()
    plt.savefig(AN / (name+'.png'), dpi=120, bbox_inches='tight')
    plt.show()


low = missing[missing.lt(5)].index.tolist()
medium = missing[missing.ge(5) & missing.le(30)].index.tolist()
high = missing[missing.gt(30)].index.tolist()
cohort = raw.dropna(subset=low).drop(columns=high).copy()
model_data = cohort.copy()  # Preserve missing values for train-only imputation.
eda = cohort.copy()
strategies = []
for column, pct in missing.items():
    if column in low:
        decision = 'Drop affected rows: under 5% missing.'
    elif column in high:
        decision = 'Drop column: over 30%; imputation would be unreliable.'
    else:
        if pd.api.types.is_numeric_dtype(eda[column]):
            eda[column] = eda[column].fillna(eda[column].median())
            decision = 'EDA median imputation: 5–30% missing; modeling fits its own training median.'
        else:
            eda[column] = eda[column].fillna(eda[column].mode().iloc[0])
            decision = 'EDA mode imputation: 5–30% missing; modeling fits its own training mode.'
    strategies.append({'column':column, 'missing_percent':pct, 'decision':decision})
strategy_table = pd.DataFrame(strategies)
print(strategy_table.to_string(index=False))
print('Retained shape:', eda.shape)
eda.to_csv(AN / 'titanic_eda.csv', index=False)
model_data.to_csv(AN / 'titanic_model_input.csv', index=False)
add_note('Missing-value decisions', strategy_table.to_markdown(index=False))
add_note('Data lineage and leakage prevention',
 'One raw load supplies one retained cohort. EDA uses its own filled view; model_data preserves original missing values in that cohort for training-fold imputation. EDA scaling is never used for modeling. The high-missing deck column is dropped. The alive column is excluded from prediction because it directly encodes the target; redundant class/who/adult_male/alone/embark_town columns are also excluded.')


outliers = {}
for column in ['age','fare']:
    fig, axes = plt.subplots(1,2,figsize=(10,3))
    sns.histplot(data=eda, x=column, kde=True, ax=axes[0])
    sns.boxplot(data=eda, x=column, ax=axes[1])
    save_plot('univariate_'+column)
    q1,q3 = eda[column].quantile([.25,.75])
    iqr = q3-q1
    outliers[column] = int(((eda[column]<q1-1.5*iqr) | (eda[column]>q3+1.5*iqr)).sum())
fare_stats = {'mean':float(eda.fare.mean()), 'median':float(eda.fare.median()),
              'modes':eda.fare.mode().tolist(), 'skewness':float(eda.fare.skew())}
print('IQR outliers:', outliers)
print('Fare statistics:', fare_stats)
add_note('Univariate results', f'IQR outlier counts: {outliers}\n\nFare statistics: {fare_stats}')
add_note('Fare interpretation', 'Fare is strongly right-skewed. The mean fare is approximately 32.10, while the median is approximately 14.45 and the mode is 8.05. Because the mean is much larger than the median and mode, a relatively small number of high fares pull the distribution to the right. These high fares are retained because they are valid passenger observations rather than confirmed data errors.')


breakdowns = []
for sex in sorted(eda.sex.unique()):
    mask = eda.sex.eq(sex) & eda.survived.notna()
    breakdowns.append({'group':'sex='+sex,'n':int(mask.sum()),'survival_rate':eda.loc[mask,'survived'].mean()})
for cls in sorted(eda.pclass.unique()):
    mask = eda.pclass.eq(cls) & eda.survived.notna()
    breakdowns.append({'group':f'pclass={cls}','n':int(mask.sum()),'survival_rate':eda.loc[mask,'survived'].mean()})
    for sex in sorted(eda.sex.unique()):
        mask = eda.sex.eq(sex) & eda.pclass.eq(cls)
        breakdowns.append({'group':f'{sex}, pclass={cls}','n':int(mask.sum()),'survival_rate':eda.loc[mask,'survived'].mean()})
rates = pd.DataFrame(breakdowns)
print(rates.to_string(index=False))
cols = ['survived','pclass','age','sibsp','parch','fare']
corr = eda[cols].corr()
plt.figure(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
save_plot('correlations')
pairs = [(cols[i],cols[j],corr.iloc[i,j]) for i in range(6) for j in range(i+1,6)]
strongest = sorted(pairs, key=lambda p:abs(p[2]), reverse=True)[:2]
print('Strongest unique pairs:', strongest)
add_note('Survival rates', rates.to_markdown(index=False))
add_note('Six-column correlations', corr.to_markdown())
add_note('Strongest pairs', str(strongest)+'\n\nThe strongest absolute correlation is between passenger class and fare, approximately -0.55. The negative direction means that numerically higher passenger-class values are associated with lower fares. SibSp and Parch have a moderate positive correlation of approximately 0.41 because passengers travelling with siblings or spouses may also travel with parents or children. These correlations describe association only and do not establish causation.')


plt.figure(figsize=(7,4))
sns.barplot(data=eda, x='pclass', y='survived', hue='sex', errorbar=None)
plt.ylabel('Survival proportion')
save_plot('story_1_class_sex')

plt.figure(figsize=(7,4))
sns.boxplot(data=eda, x='survived', y='age', hue='sex')
save_plot('story_2_age_sex')

plt.figure(figsize=(7,4))
sns.boxplot(data=eda, x='pclass', y='fare', hue='survived')
plt.yscale('symlog')
save_plot('story_3_fare_class')

story = eda.assign(family_size=eda.sibsp+eda.parch+1)
plt.figure(figsize=(8,4))
sns.barplot(data=story, x='family_size', y='survived', hue='sex', errorbar=None)
plt.ylabel('Survival proportion')
save_plot('story_4_family_sex')
print('Counts for family-size chart:\n', pd.crosstab(story.family_size,story.sex))
for number, title in enumerate(['Class and sex','Age and sex','Fare and class','Family size and sex'],1):
    add_note(f'Story chart {number}: {title}',
             'The corresponding story chart is interpreted in analytics/interpretations.md. The plots show clear differences in survival by passenger sex and class, differences in fare across classes, and additional patterns involving age and family size. These visual findings support the numerical EDA results and should be interpreted as historical associations rather than causal relationships.')


before = eda[['age','fare']]
z = (before-before.mean())/before.std(ddof=0)
check = pd.DataFrame({'before_mean':before.mean(), 'before_std':before.std(ddof=0),
                      'after_mean':z.mean(), 'after_std':z.std(ddof=0)})
print(check)
assert np.allclose(z.mean(),0,atol=1e-10)
assert np.allclose(z.std(ddof=0),1)
add_note('EDA standardization check (not model input)',check.to_markdown())


from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
 roc_auc_score, ConfusionMatrixDisplay, RocCurveDisplay, mean_absolute_error,
 mean_squared_error, r2_score)
import joblib

numeric = ['pclass','age','sibsp','parch','fare']
categorical = ['sex','embarked']
X = model_data[numeric+categorical].copy()
y = model_data.survived.astype(int)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
def preprocess(num):
    return ColumnTransformer([
      ('num',Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]),num),
      ('cat',Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),
                       ('encoder',OneHotEncoder(handle_unknown='ignore',drop='first',sparse_output=False))]),categorical)])
prep = preprocess(numeric)
balance = pd.DataFrame({'all':y.value_counts(normalize=True),
                        'train':y_train.value_counts(normalize=True),
                        'test':y_test.value_counts(normalize=True)})
print(balance)
add_note('Stratification',balance.to_markdown()+'\n\nStratification approximately preserves the observed class proportions. Numeric medians, categorical modes, one-hot encoding and scaling are fitted only inside training pipelines.')


cv = StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
estimators = {
 'Logistic Regression':LogisticRegression(max_iter=2000,random_state=42),
 'Decision Tree':DecisionTreeClassifier(max_depth=4,random_state=42),
 'Random Forest':RandomForestClassifier(n_estimators=150,random_state=42,n_jobs=1)
}
fitted, metric_rows, cv_scores = {}, [], {}
for name, estimator in estimators.items():
    pipe = Pipeline([('prep',clone(prep)),('model',estimator)])
    cv_scores[name] = float(cross_val_score(pipe,X_train,y_train,cv=cv,scoring='f1',n_jobs=-1).mean())
    pipe.fit(X_train,y_train)
    fitted[name] = pipe
    pred = pipe.predict(X_test)
    proba = pipe.predict_proba(X_test)[:,1]
    metric_rows.append({'model':name,'accuracy':accuracy_score(y_test,pred),
      'precision':precision_score(y_test,pred,zero_division=0),'recall':recall_score(y_test,pred),
      'F1':f1_score(y_test,pred),'AUC':roc_auc_score(y_test,proba)})
classification = pd.DataFrame(metric_rows).set_index('model')
print(classification)
print('Training CV F1:',cv_scores)
fig,axes = plt.subplots(1,3,figsize=(14,4))
for ax,(name,pipe) in zip(axes,fitted.items()):
    ConfusionMatrixDisplay.from_estimator(pipe,X_test,y_test,ax=ax,colorbar=False)
    ax.set_title(name)
save_plot('confusion_matrices')
fig,ax = plt.subplots(figsize=(7,5))
for name,pipe in fitted.items():
    RocCurveDisplay.from_estimator(pipe,X_test,y_test,ax=ax,name=name)
ax.plot([0,1],[0,1],'k--')
save_plot('roc_curves')
add_note('Classifier metrics',classification.to_markdown())
add_note('Training CV F1 for selection',str(cv_scores))


tree_pipe = fitted['Decision Tree']
plt.figure(figsize=(24,10))
plot_tree(tree_pipe.named_steps['model'],
          feature_names=tree_pipe.named_steps['prep'].get_feature_names_out(),
          class_names=['Not survived','Survived'],filled=True,rounded=True,fontsize=8)
save_plot('decision_tree')


from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
variants = {
 'baseline':Pipeline([('prep',clone(prep)),('model',LogisticRegression(max_iter=2000,random_state=42))]),
 'balanced':Pipeline([('prep',clone(prep)),('model',LogisticRegression(max_iter=2000,class_weight='balanced',random_state=42))]),
 'SMOTE':ImbPipeline([('prep',clone(prep)),('smote',SMOTE(random_state=42)),
                      ('model',LogisticRegression(max_iter=2000,random_state=42))])
}
imbalance_rows = []
for name,pipe in variants.items():
    cv_f1 = cross_val_score(pipe,X_train,y_train,cv=cv,scoring='f1',n_jobs=-1).mean()
    pipe.fit(X_train,y_train)
    pred = pipe.predict(X_test)
    imbalance_rows.append({'strategy':name,'CV_F1':cv_f1,
       'precision':precision_score(y_test,pred,zero_division=0),
       'recall':recall_score(y_test,pred),'F1':f1_score(y_test,pred)})
imbalance = pd.DataFrame(imbalance_rows).set_index('strategy')
print(imbalance)
add_note('Imbalance comparison',imbalance.to_markdown())
add_note('Imbalance interpretation',
 'Among the imbalance strategies, SMOTE achieved the strongest training cross-validation F1 of approximately 0.731. On the held-out test data, baseline Logistic Regression had precision about 0.797, recall about 0.691 and F1 about 0.740; the balanced model increased recall to about 0.750 but reduced precision; SMOTE produced precision about 0.746, recall about 0.735 and F1 about 0.741. SMOTE is applied only within the training pipeline to prevent information from the held-out test set leaking into model training. Because oversampling is performed after one-hot encoding, synthetic samples may contain fractional indicator values, which is a limitation of this implementation.')


search = GridSearchCV(
 Pipeline([('prep',clone(prep)),('model',RandomForestClassifier(oob_score=True,bootstrap=True,random_state=42,n_jobs=1))]),
 {'model__n_estimators':[100,200], 'model__max_depth':[None,8],
  'model__max_features':['sqrt',.8]}, scoring='f1',cv=cv,n_jobs=-1)
search.fit(X_train,y_train)
print('Best parameters:',search.best_params_)
print('Best CV F1:',search.best_score_)
print('OOB score:',search.best_estimator_.named_steps['model'].oob_score_)
fitted['Tuned Random Forest'] = search.best_estimator_
cv_scores['Tuned Random Forest'] = float(search.best_score_)
pred = search.predict(X_test)
proba = search.predict_proba(X_test)[:,1]
classification.loc['Tuned Random Forest'] = [accuracy_score(y_test,pred),
 precision_score(y_test,pred,zero_division=0),recall_score(y_test,pred),
 f1_score(y_test,pred),roc_auc_score(y_test,proba)]
add_note('Random Forest tuning',json.dumps({'parameters':search.best_params_,
 'CV_F1':float(search.best_score_),
 'OOB_score':float(search.best_estimator_.named_steps['model'].oob_score_)},indent=2))


reg_numeric = ['pclass','age','sibsp','parch']
XR = model_data[reg_numeric+categorical]
yr = model_data.fare
XR_train,XR_test = XR.loc[X_train.index],XR.loc[X_test.index]
yr_train,yr_test = yr.loc[X_train.index],yr.loc[X_test.index]
reg = Pipeline([('prep',preprocess(reg_numeric)),('model',LinearRegression())])
reg.fit(XR_train,yr_train)
fare_pred = reg.predict(XR_test)
r2 = r2_score(yr_test,fare_pred)
n = len(yr_test)
p = reg.named_steps['prep'].transform(XR_test).shape[1]
adjusted = 1-(1-r2)*(n-1)/(n-p-1) if n>p+1 else np.nan
regression = pd.DataFrame([{'model':'Linear Regression',
 'MAE':mean_absolute_error(yr_test,fare_pred),
 'RMSE':np.sqrt(mean_squared_error(yr_test,fare_pred)), 'R2':r2,'Adjusted_R2':adjusted}]).set_index('model')
print(regression)
residuals = np.asarray(yr_test)-fare_pred
plt.figure(figsize=(7,4))
plt.scatter(fare_pred,residuals,alpha=.6)
plt.axhline(0,color='black',linestyle='--')
plt.xlabel('Predicted fare'); plt.ylabel('Actual minus predicted fare')
save_plot('regression_residuals')
residual_groups = pd.DataFrame({'predicted':fare_pred,'residual':residuals})
residual_groups['predicted_quartile'] = pd.qcut(residual_groups.predicted,4,duplicates='drop')
spread = residual_groups.groupby('predicted_quartile',observed=True).residual.agg(['count','std'])
print('Residual spread by prediction bin:\n',spread)
add_note('Regression metrics',regression.to_markdown()+f'\n\nTest n={n}; transformed predictors p={p}.')
add_note('Residual spread',spread.to_markdown())
add_note('Residual interpretation',
 'The residual plot suggests that prediction errors are not perfectly constant across the fitted-fare range. The residual standard deviation increases across several prediction bins, from roughly 7.7 in the lowest fitted-fare group to around 10 or more in higher groups, indicating some evidence of non-constant variance. This visual pattern is consistent with possible heteroscedasticity, although the plot alone is not a formal statistical test.')


best_name = max(cv_scores,key=cv_scores.get)
best_pipeline = fitted[best_name]
joblib.dump(best_pipeline,AN / 'best_pipeline.joblib')
reloaded = joblib.load(AN / 'best_pipeline.joblib')
raw_example = X_test.head(5)
np.testing.assert_array_equal(best_pipeline.predict(raw_example),reloaded.predict(raw_example))
print('Selected:',best_name,'CV F1:',cv_scores[best_name])
print('Raw inputs:\n',raw_example)
print('Reloaded predictions:',reloaded.predict(raw_example))
combined = pd.concat({'Classification metrics':classification,
                      'Regression metrics':regression},axis=1)
print(combined.to_string())
combined.to_csv(AN / 'model_comparison.csv')
add_note('Final metrics — distinct groups',combined.to_markdown())
add_note('Selected pipeline',f'{best_name}; training CV F1={cv_scores[best_name]:.4f}. Reloaded raw-input predictions match.')
add_note('Final recommendation',
 'The final classifier is selected using training cross-validation F1 rather than the held-out test set. Logistic Regression achieved test accuracy of approximately 0.815, precision of approximately 0.797, recall of approximately 0.691, F1 of approximately 0.740 and ROC-AUC of approximately 0.861. The tuned Random Forest obtained the strongest training cross-validation F1, demonstrating the tradeoff between model-selection criteria and held-out performance. These models are educational models trained on the historical Titanic dataset and are not validated for real customer, safety, or business decisions.')
(AN / 'results.md').write_text('\n\n'.join(notes),encoding='utf-8')
(AN / 'README.md').write_text("# Analytics\nInstall root requirements; run `python analytics/pipeline.py` from the repository root.\nThe first run loads Titanic with Seaborn and immediately saves titanic.csv. Later runs reuse that CSV, including offline grading. The same retained cohort supplies EDA and modeling; EDA-imputed values are not fed to models. Training-only pipeline imputers preserve the evaluation boundary. alive and redundant derived flags are excluded from model inputs.\n\nresults.md contains measured results and writing prompts. interpretations.md must contain your own completed interpretations for the four story charts, correlations, skewness, imbalance, residuals and final recommendation. best_pipeline.joblib includes preprocessing and classifier and is checked on raw inputs after reloading.\n\nModel choice uses training CV F1; the tuned forest's maximum CV score can be optimistic from hyperparameter selection. The held-out test results provide a separate estimate. OOB is supplementary because preprocessing is fitted on the full training split. SMOTE after one-hot encoding can produce fractional indicators; this limitation is disclosed.\n",encoding='utf-8')
