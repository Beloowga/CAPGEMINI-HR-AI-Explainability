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
The audit showed no significant age bias in the model. DI improved from 0.954 to 1.000 and SPD from -0.032 to 0.000 after Reweighing. EOD slightly degraded (-0.034 to -0.145) : it is difficult to optimise all fairness metrics simultaneously. AOD remained within the fair threshold throughout.
    
### 3) SHAP 
#### a) What is SHAP ?
SHAP (SHapley Additive exPlanations) is a model interpretability framework that explains the predictions of machine-learning models by assigning each feature an importance value for a particular prediction. Based on concepts from Game Theory—specifically the Shapley Value—SHAP quantifies how much each input feature contributes to the difference between the model’s prediction and the average prediction. It works with many types of models and provides both global explanations (overall feature importance) and local explanations (feature contributions for individual predictions), helping practitioners better understand, trust, and debug complex models.

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

Hyperparameters were optimised using grid search / manual tuning.

Key parameters tuned:
- max_depth
- learning_rate
- n_estimators
- subsample
- colsample_bytree

The goal was to balance performance and overfitting.

### 5) Overfitting analysis

A significant gap between training and test performance was observed in XGBoost:
- Train AUC: 0.996
- Test AUC: 0.684

This indicates strong overfitting.

The final model (Random Forest) was selected due to:
- Smaller performance gap
- Better generalisation
 
