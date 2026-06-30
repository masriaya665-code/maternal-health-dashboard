import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Risk Predictor", layout="wide")
BASE = "."

@st.cache_data
def load_and_train():
    df = pd.read_csv(BASE + "/data/maternal_risk.csv")
    label_map = {"low risk": 0, "mid risk": 1, "high risk": 2}
    df["RiskEncoded"] = df["RiskLevel"].map(label_map)
    X = df[["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]]
    y = df["RiskEncoded"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    importances = pd.DataFrame({"Feature": X.columns, "Importance": model.feature_importances_}).sort_values("Importance", ascending=False)
    return model, accuracy, importances

model, accuracy, importances = load_and_train()
st.title("Maternal Risk Level Predictor")
st.markdown("Enter a patient's clinical vitals to receive a predicted risk classification.")
st.info(f"Model accuracy: **{accuracy*100:.1f}%** (Random Forest Classifier, 80/20 train-test split)")
st.markdown("---")

st.subheader("Patient Vitals Input")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=10, max_value=70, value=25)
    systolic = st.number_input("Systolic BP", min_value=70, max_value=200, value=120)
with col2:
    diastolic = st.number_input("Diastolic BP", min_value=40, max_value=150, value=80)
    bs = st.number_input("Blood Sugar (mmol/L)", min_value=5.0, max_value=20.0, value=7.0)
with col3:
    temp = st.number_input("Body Temperature (F)", min_value=97.0, max_value=105.0, value=98.0)
    hr = st.number_input("Heart Rate (bpm)", min_value=40, max_value=100, value=75)

if st.button("Predict Risk Level"):
    input_data = pd.DataFrame([[age, systolic, diastolic, bs, temp, hr]], columns=["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"])
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]
    label_map = {0: "Low Risk", 1: "Mid Risk", 2: "High Risk"}
    result = label_map[prediction]
    st.markdown("---")
    st.subheader("Prediction Result")
    if prediction == 0:
        st.success(f"Predicted Risk Level: **{result}**")
    elif prediction == 1:
        st.warning(f"Predicted Risk Level: **{result}**")
    else:
        st.error(f"Predicted Risk Level: **{result}**")
    prob_df = pd.DataFrame({"Risk Level": ["Low Risk", "Mid Risk", "High Risk"], "Probability": [proba[0], proba[1], proba[2]]})
    fig = px.bar(prob_df, x="Risk Level", y="Probability", color="Risk Level",
        color_discrete_map={"Low Risk": "#2dc653", "Mid Risk": "#f4a261", "High Risk": "#c0392b"},
        title="Prediction Confidence by Risk Level")
    fig.update_layout(yaxis_tickformat=".0%", yaxis_title="Probability")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Feature Importance")
fig2 = px.bar(importances, x="Importance", y="Feature", orientation="h",
    color_discrete_sequence=["#c0392b"],
    title="Relative Importance of Clinical Features")
st.plotly_chart(fig2, use_container_width=True)
