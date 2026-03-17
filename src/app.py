import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# ------------------------------------------------
# Load model (cached)
# ------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("random_forest_model.pkl")

model = load_model()
explainer = shap.TreeExplainer(model)

# ------------------------------------------------
# Load datasets
# ------------------------------------------------

df_original = pd.read_csv("HRDataset_v14.csv")
df_cleaned = pd.read_csv("hr_cleaned.csv")

feature_columns = df_cleaned.drop(columns="Termd").columns

# ------------------------------------------------
# App title
# ------------------------------------------------

st.title("Employee Termination Prediction")
st.write("Predict whether an employee is likely to leave the company.")

# ------------------------------------------------
# Employee inputs
# ------------------------------------------------

st.header("Employee Information")

age = st.number_input("Age", 18, 70)
salary = st.number_input("Salary", 30000, 200000)

engagement = st.slider("Engagement Survey", 0.0, 5.0)
satisfaction = st.slider("Employee Satisfaction", 1, 5)

projects = st.number_input("Special Projects Count", 0, 20)
late = st.number_input("Days Late Last 30", 0, 30)
absences = st.number_input("Absences", 0, 50)

# ------------------------------------------------
# Dropdown values from original dataset
# ------------------------------------------------

departments = df_original["Department"].dropna().unique()
department = st.selectbox("Department", departments)

positions = df_original["Position"].dropna().unique()
position = st.selectbox("Position", positions)

managers = df_original["ManagerName"].dropna().unique()
manager = st.selectbox("Manager", managers)

recruitment_sources = df_original["RecruitmentSource"].dropna().unique()
recruitment = st.selectbox("Recruitment Source", recruitment_sources)

citizenship = df_original["CitizenDesc"].dropna().unique()
citizen = st.selectbox("Citizenship", citizenship)

married = st.selectbox("Married", ["Yes", "No"])
married_id = 1 if married == "Yes" else 0

# ------------------------------------------------
# Convert text inputs → IDs
# ------------------------------------------------

dept_id = df_original[df_original["Department"] == department]["DeptID"].iloc[0]

position_id = df_original[df_original["Position"] == position]["PositionID"].iloc[0]

manager_id = df_original[df_original["ManagerName"] == manager]["ManagerID"].iloc[0]

# ------------------------------------------------
# Citizen encoding
# ------------------------------------------------

citizen_us = 1 if citizen == "US Citizen" else 0
citizen_non = 1 if citizen != "US Citizen" else 0

# ------------------------------------------------
# Recruitment source one-hot
# ------------------------------------------------

recruitment_cols = [c for c in df_cleaned.columns if "RecruitmentSource_" in c]

recruitment_data = {col: 0 for col in recruitment_cols}

selected_col = f"RecruitmentSource_{recruitment}"

if selected_col in recruitment_data:
    recruitment_data[selected_col] = 1

# ------------------------------------------------
# Build input dataframe
# ------------------------------------------------

data = {
    "MarriedID":[married_id],
    "MaritalStatusID":[married_id],
    "DeptID":[dept_id],
    "PerfScoreID":[3],
    "FromDiversityJobFairID":[0],
    "Salary":[salary],
    "PositionID":[position_id],
    "ManagerID":[manager_id],
    "EngagementSurvey":[engagement],
    "EmpSatisfaction":[satisfaction],
    "SpecialProjectsCount":[projects],
    "DaysLateLast30":[late],
    "Absences":[absences],
    "Age":[age],
    "CitizenDesc_Non-Citizen":[citizen_non],
    "CitizenDesc_US Citizen":[citizen_us]
}

data.update(recruitment_data)

df_input = pd.DataFrame(data)

# Ensure column order exactly matches training
df_input = df_input[feature_columns]

# ------------------------------------------------
# Prediction
# ------------------------------------------------

st.header("Prediction")

if st.button("Predict"):

    prediction = model.predict(df_input)[0]
    prob = model.predict_proba(df_input)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Employee likely to leave (probability {prob:.2f})")
    else:
        st.success(f"✅ Employee likely to stay (probability {1-prob:.2f})")

# ------------------------------------------------
# SHAP explanation
# ------------------------------------------------

    st.header("Prediction Explanation (SHAP)")

    shap_values = explainer.shap_values(df_input)

    if isinstance(shap_values, list):
        sv = shap_values[1][0]
        base_value = explainer.expected_value[1]
    else:
        sv = shap_values[0, :, 1]
        base_value = explainer.expected_value[1]

    explanation = shap.Explanation(
        values=sv,
        base_values=base_value,
        data=df_input.iloc[0],
        feature_names=df_input.columns
    )

    fig, ax = plt.subplots()

    shap.plots.waterfall(explanation, show=False)

    st.pyplot(fig)
