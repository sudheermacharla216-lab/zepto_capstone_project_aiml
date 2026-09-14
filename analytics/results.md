# Analytics results

## Profile

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 891 entries, 0 to 890
Data columns (total 15 columns):
 #   Column       Non-Null Count  Dtype   
---  ------       --------------  -----   
 0   survived     891 non-null    int64   
 1   pclass       891 non-null    int64   
 2   sex          891 non-null    object  
 3   age          714 non-null    float64 
 4   sibsp        891 non-null    int64   
 5   parch        891 non-null    int64   
 6   fare         891 non-null    float64 
 7   embarked     889 non-null    object  
 8   class        891 non-null    category
 9   who          891 non-null    object  
 10  adult_male   891 non-null    bool    
 11  deck         203 non-null    category
 12  embark_town  889 non-null    object  
 13  alive        891 non-null    object  
 14  alone        891 non-null    bool    
dtypes: bool(2), category(2), float64(2), int64(4), object(5)
memory usage: 80.7+ KB

```

|       |   survived |     pclass |      age |      sibsp |      parch |     fare |
|:------|-----------:|-----------:|---------:|-----------:|-----------:|---------:|
| count | 891        | 891        | 714      | 891        | 891        | 891      |
| mean  |   0.383838 |   2.30864  |  29.6991 |   0.523008 |   0.381594 |  32.2042 |
| std   |   0.486592 |   0.836071 |  14.5265 |   1.10274  |   0.806057 |  49.6934 |
| min   |   0        |   1        |   0.42   |   0        |   0        |   0      |
| 25%   |   0        |   2        |  20.125  |   0        |   0        |   7.9104 |
| 50%   |   0        |   3        |  28      |   0        |   0        |  14.4542 |
| 75%   |   1        |   3        |  38      |   1        |   0        |  31      |
| max   |   1        |   3        |  80      |   8        |   6        | 512.329  |

Shape: (891, 15)

|             |   missing_percent |
|:------------|------------------:|
| deck        |         77.2166   |
| age         |         19.8653   |
| embarked    |          0.224467 |
| embark_town |          0.224467 |

|   survived |   fraction |
|-----------:|-----------:|
|          0 |   0.616162 |
|          1 |   0.383838 |

## Missing-value decisions

| column      |   missing_percent | decision                                                                     |
|:------------|------------------:|:-----------------------------------------------------------------------------|
| deck        |         77.2166   | Drop column: over 30%; imputation would be unreliable.                       |
| age         |         19.8653   | EDA median imputation: 5–30% missing; modeling fits its own training median. |
| embarked    |          0.224467 | Drop affected rows: under 5% missing.                                        |
| embark_town |          0.224467 | Drop affected rows: under 5% missing.                                        |

## Data lineage and leakage prevention

One raw load supplies one retained cohort. EDA uses its own filled view; model_data preserves original missing values in that cohort for training-fold imputation. EDA scaling is never used for modeling. The high-missing deck column is dropped. The alive column is excluded from prediction because it directly encodes the target; redundant class/who/adult_male/alone/embark_town columns are also excluded.

## Univariate results

IQR outlier counts: {'age': 65, 'fare': 114}

Fare statistics: {'mean': 32.09668087739032, 'median': 14.4542, 'modes': [8.05], 'skewness': 4.801440211044194}

## Fare interpretation

Fare is strongly right-skewed. The mean fare is approximately 32.10, the median approximately 14.45 and the mode 8.05. The much larger mean reflects a smaller number of valid high-fare passengers, so these observations were retained rather than automatically treated as errors.

## Survival rates

| group            |   n |   survival_rate |
|:-----------------|----:|----------------:|
| sex=female       | 312 |        0.740385 |
| sex=male         | 577 |        0.188908 |
| pclass=1         | 214 |        0.626168 |
| female, pclass=1 |  92 |        0.967391 |
| male, pclass=1   | 122 |        0.368852 |
| pclass=2         | 184 |        0.472826 |
| female, pclass=2 |  76 |        0.921053 |
| male, pclass=2   | 108 |        0.157407 |
| pclass=3         | 491 |        0.242363 |
| female, pclass=3 | 144 |        0.5      |
| male, pclass=3   | 347 |        0.135447 |

## Six-column correlations

|          |   survived |     pclass |        age |      sibsp |      parch |       fare |
|:---------|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| survived |  1         | -0.335549  | -0.0698217 | -0.03404   |  0.0831508 |  0.25529   |
| pclass   | -0.335549  |  1         | -0.336512  |  0.0816556 |  0.0168245 | -0.548193  |
| age      | -0.0698217 | -0.336512  |  1         | -0.232543  | -0.171485  |  0.0937071 |
| sibsp    | -0.03404   |  0.0816556 | -0.232543  |  1         |  0.414542  |  0.160887  |
| parch    |  0.0831508 |  0.0168245 | -0.171485  |  0.414542  |  1         |  0.217532  |
| fare     |  0.25529   | -0.548193  |  0.0937071 |  0.160887  |  0.217532  |  1         |

## Strongest pairs

[('pclass', 'fare', np.float64(-0.5481932852366449)), ('sibsp', 'parch', np.float64(0.4145416380997264))]

Passenger class and fare have the strongest relationship, approximately -0.55, showing that numerically higher class values are associated with lower fares. SibSp and Parch have a moderate positive relationship of approximately 0.41. These are associations and do not establish causation.

## Story chart 1: Class and sex

The chart-specific interpretation is provided in interpretations.md. Overall, survival varies strongly by passenger sex and class, fares differ substantially by class, and age and family size provide additional historical patterns.

## Story chart 2: Age and sex

The chart-specific interpretation is provided in interpretations.md. Overall, survival varies strongly by passenger sex and class, fares differ substantially by class, and age and family size provide additional historical patterns.

## Story chart 3: Fare and class

The chart-specific interpretation is provided in interpretations.md. Overall, survival varies strongly by passenger sex and class, fares differ substantially by class, and age and family size provide additional historical patterns.

## Story chart 4: Family size and sex

The chart-specific interpretation is provided in interpretations.md. Overall, survival varies strongly by passenger sex and class, fares differ substantially by class, and age and family size provide additional historical patterns.

## EDA standardization check (not model input)

|      |   before_mean |   before_std |   after_mean |   after_std |
|:-----|--------------:|-------------:|-------------:|------------:|
| age  |       29.3152 |      12.9776 |  2.67752e-16 |           1 |
| fare |       32.0967 |      49.6695 |  1.25884e-16 |           1 |

## Stratification

|   survived |      all |   train |     test |
|-----------:|---------:|--------:|---------:|
|          0 | 0.617548 | 0.61744 | 0.617978 |
|          1 | 0.382452 | 0.38256 | 0.382022 |

Stratification approximately preserves the observed class proportions. Numeric medians, categorical modes, one-hot encoding and scaling are fitted only inside training pipelines.

## Classifier metrics

| model               |   accuracy |   precision |   recall |       F1 |      AUC |
|:--------------------|-----------:|------------:|---------:|---------:|---------:|
| Logistic Regression |   0.814607 |    0.79661  | 0.691176 | 0.740157 | 0.860963 |
| Decision Tree       |   0.808989 |    0.814815 | 0.647059 | 0.721311 | 0.856016 |
| Random Forest       |   0.803371 |    0.761905 | 0.705882 | 0.732824 | 0.83008  |

## Training CV F1 for selection

{'Logistic Regression': 0.7099713431207411, 'Decision Tree': 0.7053899836737239, 'Random Forest': 0.7605456634753349}

## Imbalance comparison

| strategy   |    CV_F1 |   precision |   recall |       F1 |
|:-----------|---------:|------------:|---------:|---------:|
| baseline   | 0.709971 |    0.79661  | 0.691176 | 0.740157 |
| balanced   | 0.724585 |    0.708333 | 0.75     | 0.728571 |
| SMOTE      | 0.730814 |    0.746269 | 0.735294 | 0.740741 |

## Imbalance interpretation

SMOTE produced the highest cross-validation F1 among the three imbalance strategies at approximately 0.731. The baseline, balanced and SMOTE approaches show different precision-recall tradeoffs. SMOTE is performed only during training to prevent leakage from the held-out test set.

## Random Forest tuning

{
  "parameters": {
    "model__max_depth": 8,
    "model__max_features": 0.8,
    "model__n_estimators": 100
  },
  "CV_F1": 0.771414773113839,
  "OOB_score": 0.8185654008438819
}

## Regression metrics

| model             |     MAE |    RMSE |       R2 |   Adjusted_R2 |
|:------------------|--------:|--------:|---------:|--------------:|
| Linear Regression | 19.6457 | 41.2628 | 0.347379 |      0.320506 |

Test n=178; transformed predictors p=7.

## Residual spread

| predicted_quartile   |   count |      std |
|:---------------------|--------:|---------:|
| (-4.444, 2.355]      |      46 |  7.68404 |
| (2.355, 29.485]      |      43 |  9.9411  |
| (29.485, 61.64]      |      45 | 10.2475  |
| (61.64, 101.656]     |      44 | 77.7809  |

## Residual interpretation

The residual spread changes across fitted-fare groups, suggesting some evidence of heteroscedasticity. Residual standard deviation is about 7.7 in the lowest prediction group and rises to around 10 or more in higher groups. This is a visual diagnosis rather than a formal statistical test.

## Final metrics — distinct groups

| model               |   ('Classification metrics', 'accuracy') |   ('Classification metrics', 'precision') |   ('Classification metrics', 'recall') |   ('Classification metrics', 'F1') |   ('Classification metrics', 'AUC') |   ('Regression metrics', 'MAE') |   ('Regression metrics', 'RMSE') |   ('Regression metrics', 'R2') |   ('Regression metrics', 'Adjusted_R2') |
|:--------------------|-----------------------------------------:|------------------------------------------:|---------------------------------------:|-----------------------------------:|------------------------------------:|--------------------------------:|---------------------------------:|-------------------------------:|----------------------------------------:|
| Logistic Regression |                                 0.814607 |                                  0.79661  |                               0.691176 |                           0.740157 |                            0.860963 |                        nan      |                         nan      |                     nan        |                              nan        |
| Decision Tree       |                                 0.808989 |                                  0.814815 |                               0.647059 |                           0.721311 |                            0.856016 |                        nan      |                         nan      |                     nan        |                              nan        |
| Random Forest       |                                 0.803371 |                                  0.761905 |                               0.705882 |                           0.732824 |                            0.83008  |                        nan      |                         nan      |                     nan        |                              nan        |
| Tuned Random Forest |                                 0.825843 |                                  0.824561 |                               0.691176 |                           0.752    |                            0.838102 |                        nan      |                         nan      |                     nan        |                              nan        |
| Linear Regression   |                               nan        |                                nan        |                             nan        |                         nan        |                          nan        |                         19.6457 |                          41.2628 |                       0.347379 |                                0.320506 |

## Selected pipeline

Tuned Random Forest; training CV F1=0.7714. Reloaded raw-input predictions match.

## Final recommendation

Model selection is based on training cross-validation F1. Logistic Regression achieved approximately 0.815 accuracy, 0.797 precision, 0.691 recall, 0.740 F1 and 0.861 ROC-AUC on the test set. The tuned Random Forest achieved the strongest training CV F1, illustrating that model selection involves performance tradeoffs. The Titanic dataset is historical and this educational model is not validated for real-world customer decisions.