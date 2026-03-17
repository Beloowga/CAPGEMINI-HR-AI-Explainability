# Technical Overview

## I - AI Explainability and AI ethics
### 1) Our ethical goals:
- Guarantee a diversified dataset
- Verify data distribution notably for features such as genres, skin colour, etc..
- Focus on model explainability
- Ai fairness 360
- AI act

### 2) AIF 360 tools
#### a) What is AIF 360 ?
AI Fairness 360 (AIF360) is an open-source toolkit developed by IBM to help detect, understand, and mitigate bias in machine-learning models. It provides a comprehensive set of fairness metrics that measure potential discrimination in datasets and model predictions, as well as algorithms designed to reduce bias during different stages of the machine-learning pipeline (pre-processing, in-processing, and post-processing). AIF360 also includes example datasets, tutorials, and visualisation tools, enabling data scientists to evaluate fairness and build more transparent and responsible AI systems. In the scope of this project we use the tools provided to evaluate the bias and ethics of our models as well as the libraries allowing us to corrects these biases.

#### b) Legal context
Under GDPR Article 9 and the EU AI Act, processing categories of personal data (including gender, racial or ethnic origin) for automated decision-making in employment contexts is prohibited. These attributes were removed from the model and excluded from the bias audit. The only sensitive attribute audited is Age, as employees aged 45 and over show a consistently higher turnover rate in our dataset, making it a meaningful and legally permitted variable for bias detection.

#### c) Metrics used
We measure bias using four standard fairness metrics:

- **Disparate Impact (DI):** ratio of termination rates between the two age groups. Fair if ≥ 0.8.
- **Statistical Parity Difference (SPD):** absolute gap in termination rates between groups. Fair if |x| < 0.1.
- **Equal Opportunity Difference (EOD):** measures whether the model is equally good at identifying actual leavers across both groups. Fair if |x| < 0.1.
- **Average Odds Difference (AOD):** combines true positive and false positive rate parity across groups. Fair if |x| < 0.1.

#### d) Mitigation: Reweighing
We applied Reweighing, a pre-processing technique that assigns corrected weights to training examples to compensate for group imbalance. It does not modify any data values, it only adjusts how much the model pays attention to each example during training. The model was then retrained using these corrected weights.

#### e) Results
The fairness audit did not reveal strong evidence of age bias according to most of the selected AIF360 metrics. Reweighing improved some parity indicators, although Equal Opportunity Difference slightly degraded, illustrating the trade-offs between fairness criteria. DI improved from 0.954 to 1.000 and SPD from -0.032 to 0.000 after Reweighing. EOD slightly degraded (-0.034 to -0.145) : it is difficult to optimise all fairness metrics simultaneously. AOD remained within the fair threshold throughout.
    
### 3) SHAP 
#### a) What is SHAP ?
SHAP (SHapley Additive exPlanations) is a model interpretability framework that explains the predictions of machine-learning models by assigning each feature an importance value for a particular prediction. Based on concepts from Game Theory—specifically the Shapley Value—SHAP quantifies how much each input feature contributes to the difference between the model’s prediction and the average prediction. It works with many types of models and provides both global explanations (overall feature importance) and local explanations (feature contributions for individual predictions), helping practitioners better understand, trust, and debug complex models.

#### b) SHAP results in our project

SHAP was applied to the Random Forest model to provide local explanations for individual predictions.

For one analysed employee:
- Base value: **0.4977**
- Predicted probability: **0.459**
- Predicted class: **Active**

The most influential features observed in the notebook include:
- Recruitment source
- ManagerID
- MarriedID
- DaysLateLast30
- Salary
- SpecialProjectsCount

These explanations help identify which factors contributed most to a given prediction, improving transparency for HR users.

### 4) AI Act risk classification

This system falls under **high-risk AI systems** according to the EU AI Act, as it is used in an employment context (HR decision support).

Implications:
- Human-in-the-loop decision making is mandatory
- Model decisions must be explainable
- Bias must be monitored continuously
- Documentation and auditability are required

### 5) Limitations of interpretability

The model identifies statistical correlations between features and employee turnover.

However, these relationships **must not be interpreted as causal**.  
For example, a feature such as salary or lateness may be correlated with resignation but does not necessarily cause it.

Human expertise is required to interpret results correctly.



## II - Data
The original kaggle dataset used can be found at the following link : [Human Ressources Dataset](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)
### 1) Preprocessing
The notebooks begin by loading the HR dataset (HRDataset_v14.csv) using the pandas library and performing an initial exploration of the data structure. The exploration notebook inspects the dataset using methods such as head(), info(), describe(), and duplicate checks to understand the variables, their data types, and basic statistical properties. Visual exploration is also performed using matplotlib and seaborn, with count plots and value counts used to analyse the distribution of key demographic and employment variables such as gender, marital status, race, recruitment source, and employment status. This step helps identify patterns, potential imbalances, and variables that may be relevant for later modelling and fairness analysis.

The preprocessing notebook then prepares the data for modelling by cleaning and restructuring the dataset. Columns that could introduce data leakage, such as termination-related variables (e.g., termination date or employment status), are removed because they reveal information about the target outcome. The dataset is also prepared for machine learning by transforming categorical variables into numerical representations, typically through one-hot encoding, allowing algorithms to process them effectively. These preprocessing steps ensure that the dataset is consistent, free from leakage, and suitable for training predictive models and conducting further fairness and explainability analyses.

### 2) Data splitting

The dataset was split into:
- Training set: 80%
- Test set: 20%

Stratification was applied to preserve the class distribution (termination vs non-termination).

### 3) Class imbalance

The dataset is imbalanced (~30% leavers vs ~70% non-leavers).

To address this:
- Evaluation metrics such as F1-score and Recall were prioritised
- Model performance was analysed specifically on the minority class
- Reweighing (AIF360) was applied for fairness correction

### 4) Feature engineering

- One-hot encoding applied to categorical variables
- Removal of leakage features (e.g. termination-related variables)
- Normalisation not required for tree-based models
- Potential aggregation features (e.g. lateness frequency) retained as-is

## III - Models used
### 1)Random Forest
#### a) Overview
Random Forest is a machine-learning algorithm that builds many decision trees using random subsets of the data and features. Each tree produces a prediction, and the final result is obtained by combining them—typically through majority voting for classification or averaging for regression. This ensemble approach improves accuracy and reduces overfitting compared with a single decision tree.
#### b) Advantages
Random Forest offers several advantages for explainability compared with many other machine-learning models. First, it provides feature importance measures, which indicate how much each variable contributes to the model’s predictions. This helps identify which factors most strongly influence the outcome.

Second, although the model is composed of many trees, each individual decision tree follows a sequence of clear rules based on feature splits. This structure allows analysts to inspect trees or analyse feature contributions to understand how predictions are formed. As a result, random forests provide a balance between strong predictive performance and a level of interpretability that supports model transparency and analysis.

#### c) Limitations
Random Forest also has several limitations in terms of explainability. Although it is more interpretable than some models, the combination of many trees makes the overall model difficult to interpret globally, as there is no single clear decision path.

Additionally, its feature importance measures can be biased, particularly when features are correlated or have different scales, which may lead to misleading conclusions. While individual trees can be inspected, they are often too numerous and complex to analyse effectively. As a result, external tools such as SHAP are often needed to gain deeper and more reliable insights.

### 2)XGBoost
#### a) Overview
XGBoost is a machine-learning algorithm that builds decision trees sequentially, where each new tree focuses on correcting the errors of the previous ones. By optimising a loss function and adding regularisation, it improves accuracy while controlling overfitting, making it highly effective for structured data.

#### b) Advantages
XGBoost offers several advantages for explainability despite being a powerful ensemble model. It provides built-in feature importance scores, helping identify which variables most influence predictions. In addition, its tree-based structure allows for detailed analysis of how features are used across splits, giving insight into decision patterns.

Moreover, XGBoost works particularly well with interpretability tools such as SHAP, which can break down predictions into individual feature contributions. This makes it possible to obtain both global explanations (overall model behaviour) and local explanations (why a specific prediction was made), improving transparency and trust in the model.

#### c) Limitations
XGBoost has several limitations when it comes to explainability. First, as an ensemble of many sequential trees, it is inherently complex and less interpretable than simpler models like a single decision tree, making it difficult to directly understand how predictions are formed.

Second, its feature importance measures can sometimes be misleading or biased, especially when features are correlated, as importance may be distributed unevenly. While tools like SHAP help improve interpretability, they add an extra layer of complexity and can be computationally expensive. Overall, understanding XGBoost often requires additional methods and expertise, which can limit its transparency in practice.

### 3) Model selection rationale

Tree-based models were selected because:
- They handle tabular data effectively
- They require minimal preprocessing
- They provide built-in interpretability (feature importance)
- They are compatible with SHAP for deeper explanations
  
### 4) Hyperparameter tuning

Hyperparameters were optimised using RandomizedSearchCV for XGBoost.

Key parameters tuned:
- max_depth
- learning_rate
- n_estimators
- min_child_weight
- subsample
- colsample_bytree
- gamma

Best parameters found:
- subsample = 0.8
- n_estimators = 400
- min_child_weight = 3
- max_depth = 5
- learning_rate = 0.01
- gamma = 0
- colsample_bytree = 0.6

Best cross-validated ROC-AUC for XGBoost: **0.651**

The goal was to balance predictive performance and overfitting.

### 5) Overfitting analysis

A significant gap between training and test performance was observed for XGBoost:
- Train AUC: **0.991**
- Test AUC: **0.696**
- Gap: **0.295**

This indicates substantial overfitting despite hyperparameter tuning.

A smaller but still noticeable gap was observed for Random Forest:
- Train AUC: **0.882**
- Test AUC: **0.778**
- Gap: **0.105**

This suggests moderate overfitting, but with better generalisation than XGBoost.

The final model (Random Forest) was selected because it achieved:
- the best overall test performance,
- better class balance on the minority class,
- and a more acceptable generalisation trade-off.

 ## IV - Evaluation

### 1) Performance metrics rationale

The following metrics were used to evaluate the models:

- **Accuracy**: overall proportion of correct predictions
- **Precision**: reliability of positive predictions
- **Recall**: ability to identify employees who actually leave
- **F1-score**: harmonic mean of precision and recall
- **ROC-AUC**: overall ability to distinguish between leavers and non-leavers

In this use case, **Recall** is particularly important because failing to identify employees at risk of leaving may reduce the practical usefulness of the model. However, Recall must be balanced with Precision to avoid too many false alerts.

---

### 2) Baseline model results

The baseline model is a **Logistic Regression pipeline**.

#### Cross-validation (5-fold)
- Accuracy: **0.657 ± 0.044**
- F1-score: **0.554 ± 0.049**

#### Test set results

| Class | Precision | Recall | F1-score | Support |
|------|----------:|-------:|---------:|--------:|
| Active (0) | 0.79 | 0.64 | 0.71 | 42 |
| Terminated (1) | 0.48 | 0.67 | 0.56 | 21 |

- **Accuracy:** 0.65

The baseline model shows relatively good Recall on the “Terminated” class, but weak Precision, meaning that many employees predicted as likely to leave would in fact remain.

---

### 3) XGBoost results

XGBoost was tuned using RandomizedSearchCV.

#### Best hyperparameters
- subsample = 0.8
- n_estimators = 400
- min_child_weight = 3
- max_depth = 5
- learning_rate = 0.01
- gamma = 0
- colsample_bytree = 0.6

#### Validation
- Best CV ROC-AUC: **0.651**

#### Test set results

| Class | Precision | Recall | F1-score | Support |
|------|----------:|-------:|---------:|--------:|
| Active (0) | 0.75 | 0.79 | 0.77 | 42 |
| Terminated (1) | 0.53 | 0.48 | 0.50 | 21 |

- **Accuracy:** 0.68
- **ROC-AUC:** 0.696

#### Overfitting check
- Train AUC: **0.991**
- Test AUC: **0.696**
- Gap: **0.295**

Although XGBoost improved overall discrimination compared with the baseline, it showed a strong overfitting effect and weaker Recall on the minority class than the baseline.

---

### 4) Random Forest results

The Random Forest model achieved the best overall balance between predictive performance and generalisation.

#### Test set results

| Class | Precision | Recall | F1-score | Support |
|------|----------:|-------:|---------:|--------:|
| Active (0) | 0.80 | 0.86 | 0.83 | 42 |
| Terminated (1) | 0.67 | 0.57 | 0.62 | 21 |

- **Accuracy:** 0.76
- **ROC-AUC:** 0.778

#### Overfitting check
- Train AUC: **0.882**
- Test AUC: **0.778**
- Gap: **0.105**

Compared with the other models, Random Forest delivered:
- the highest test accuracy,
- the highest ROC-AUC,
- the best Precision on the “Terminated” class,
- and a more controlled overfitting profile than XGBoost.

---

### 5) Model comparison

| Model | Accuracy | ROC-AUC | Terminated Precision | Terminated Recall | Terminated F1 | Notes |
|------|---------:|--------:|---------------------:|------------------:|--------------:|------|
| Baseline (Logistic Regression) | 0.65 | - | 0.48 | 0.67 | 0.56 | Better Recall, weaker Precision |
| XGBoost | 0.68 | 0.696 | 0.53 | 0.48 | 0.50 | Strong overfitting |
| Random Forest | 0.76 | 0.778 | 0.67 | 0.57 | 0.62 | Best trade-off |

---

### 6) Final model selection

The **Random Forest** model was selected as the final model because it provided the best overall compromise between:

- predictive performance,
- generalisation ability,
- interpretability,
- and robustness on the minority class.

Although the baseline logistic regression achieved slightly better Recall on employees who leave, Random Forest produced a better overall balance and fewer false positives, which makes it more suitable for HR decision support.

## V - Pipeline architecture

1. Data loading (CSV)
2. Data exploration
3. Preprocessing (cleaning, encoding)
4. Train/test split
5. Model training
6. Bias analysis (AIF360)
7. Model evaluation
8. Explainability (SHAP)

## VI - Deployment considerations

- Model can be deployed as an API for HR tools
- Predictions should always be reviewed by HR professionals
- Regular retraining is required to avoid data drift
- Monitoring of fairness metrics is necessary in production
