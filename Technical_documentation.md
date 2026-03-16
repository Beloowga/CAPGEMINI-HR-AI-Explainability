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

#### c) Limitations
### 2)XGBoost
 
