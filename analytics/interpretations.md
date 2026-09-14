# My interpretations

## Fare shape
The Fare distribution is positively (right) skewed. Most passengers paid relatively low fares, while a smaller number of passengers paid very high fares, creating a long right tail. The box plot also shows several high-fare outliers.

## Strongest correlations
The correlation analysis shows that survival is associated with several passenger characteristics. Passenger class and fare are also related because higher-class passengers generally paid higher fares. Family-related variables are naturally correlated.

## Chart 1 — class and sex
Survival differs clearly across passenger class and sex. Female passengers show substantially higher survival rates than male passengers, while passengers in higher classes generally have better survival outcomes than those in lower classes.

## Chart 2 — age and sex
The age distribution shows passengers across a wide range of ages, with many concentrated in the young-adult and middle-age groups. Survival patterns also differ between male and female passengers. Sex appears to provide a stronger separation in survival than age alone.

## Chart 3 — fare and class
Fare varies substantially by passenger class. First-class passengers generally paid much higher fares, while third-class passengers tended to pay lower fares. This confirms a strong relationship between fare and passenger class.

## Chart 4 — family size and sex
Family size provides additional information about passenger survival. Passengers travelling alone and those travelling with families show different survival patterns, while sex remains an important factor across family-size groups.

## Imbalance comparison
The class-imbalance experiments show that changing the class distribution or class weights affects the balance between precision and recall. The baseline model provides a useful reference, while class_weight='balanced' and SMOTE place greater emphasis on the minority class. The comparison demonstrates that imbalance handling should be selected using multiple evaluation metrics rather than accuracy alone. SMOTE was applied only to the training data to avoid data leakage.

## Regression residuals
The multivariate linear regression achieved an MAE of approximately 19.65 and an RMSE of approximately 41.26. The R² value of approximately 0.347 indicates that the model explains about 34.7% of the variation in passenger fare. The adjusted R² is approximately 0.321. The larger RMSE compared with MAE suggests that some observations have relatively large prediction errors.

## Final recommendation
Based on the model comparison, Logistic Regression is recommended as the final classification model. It achieved the highest overall accuracy of approximately 81.5%, an F1 score of approximately 0.740, and ROC-AUC of approximately 0.861 among the three baseline models. The tuned Random Forest achieved a best cross-validation F1 score of approximately 0.771 and an OOB score of approximately 0.819. Logistic Regression therefore provides a strong balance of predictive performance and interpretability.