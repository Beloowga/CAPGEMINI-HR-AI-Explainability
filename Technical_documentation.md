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
    
### 3) SHAP 
#### a) What is SHAP ?
SHAP (SHapley Additive exPlanations) is a model interpretability framework that explains the predictions of machine-learning models by assigning each feature an importance value for a particular prediction. Based on concepts from Game Theory—specifically the Shapley Value—SHAP quantifies how much each input feature contributes to the difference between the model’s prediction and the average prediction. It works with many types of models and provides both global explanations (overall feature importance) and local explanations (feature contributions for individual predictions), helping practitioners better understand, trust, and debug complex models.

## II - Data
The original kaggle dataset used can be found at the following link : [Human Ressources Dataset](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)
### 1) Preprocessing
The notebooks begin by loading the HR dataset (HRDataset_v14.csv) using the pandas library and performing an initial exploration of the data structure. The exploration notebook inspects the dataset using methods such as head(), info(), describe(), and duplicate checks to understand the variables, their data types, and basic statistical properties. Visual exploration is also performed using matplotlib and seaborn, with count plots and value counts used to analyse the distribution of key demographic and employment variables such as gender, marital status, race, recruitment source, and employment status. This step helps identify patterns, potential imbalances, and variables that may be relevant for later modelling and fairness analysis.

The preprocessing notebook then prepares the data for modelling by cleaning and restructuring the dataset. Columns that could introduce data leakage, such as termination-related variables (e.g., termination date or employment status), are removed because they reveal information about the target outcome. The dataset is also prepared for machine learning by transforming categorical variables into numerical representations, typically through one-hot encoding, allowing algorithms to process them effectively. These preprocessing steps ensure that the dataset is consistent, free from leakage, and suitable for training predictive models and conducting further fairness and explainability analyses.
### 2) Generated rows

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

#### d)Results

### 2)XGBoost
#### a) Overview
XGBoost is a machine-learning algorithm that builds decision trees sequentially, where each new tree focuses on correcting the errors of the previous ones. By optimising a loss function and adding regularisation, it improves accuracy while controlling overfitting, making it highly effective for structured data.

#### b) Advantages
XGBoost offers several advantages for explainability despite being a powerful ensemble model. It provides built-in feature importance scores, helping identify which variables most influence predictions. In addition, its tree-based structure allows for detailed analysis of how features are used across splits, giving insight into decision patterns.

Moreover, XGBoost works particularly well with interpretability tools such as SHAP, which can break down predictions into individual feature contributions. This makes it possible to obtain both global explanations (overall model behaviour) and local explanations (why a specific prediction was made), improving transparency and trust in the model.

#### c) Limitations
XGBoost has several limitations when it comes to explainability. First, as an ensemble of many sequential trees, it is inherently complex and less interpretable than simpler models like a single decision tree, making it difficult to directly understand how predictions are formed.

Second, its feature importance measures can sometimes be misleading or biased, especially when features are correlated, as importance may be distributed unevenly. While tools like SHAP help improve interpretability, they add an extra layer of complexity and can be computationally expensive. Overall, understanding XGBoost often requires additional methods and expertise, which can limit its transparency in practice.
#### d) Results

 
