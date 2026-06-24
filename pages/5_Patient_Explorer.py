import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Patient Explorer", layout="wide")

BASE = "."

@st.cache_data
def load_risk():
    return pd.read_csv(BASE + "/data/maternal_risk.csv")

df = load_risk()

st.title("Patient Data Explorer")
st.markdown("Explore individual patient vitals from the Maternal Health Risk dataset.")

st.sidebar.header("Filters")
age_range = st.sidebar.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (15, 50))
risk_levels = st.sidebar.multiselect("Risk Level", df["RiskLevel"].unique().tolist(),
                                      default=df["RiskLevel"].unique().tolist())

filtered = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1]) &
              (df["RiskLevel"].isin(risk_levels))]

st.markdown(f"Showing **{len(filtered)}** of **{len(df)}** patients")
st.markdown("---")

st.subheader("Age Distribution by Risk Level")
fig1 = px.histogram(filtered, x="Age", color="RiskLevel",
                    color_discrete_map={"low risk": "#2dc653", "mid risk": "#f4a261", "high risk": "#c0392b"},
                    barmode="overlay", nbins=30,
                    title="Age Distribution by Risk Level")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

st.subheader("Blood Pressure vs Blood Sugar")
fig2 = px.scatter(filtered, x="SystolicBP", y="BS", color="RiskLevel",
                  color_discrete_map={"low risk": "#2dc653", "mid risk": "#f4a261", "high risk": "#c0392b"},
                  hover_data=["Age", "HeartRate", "BodyTemp"],
                  title="Systolic Blood Pressure vs Blood Sugar by Risk Level")
fig2.update_layout(xaxis_title="Systolic BP", yaxis_title="Blood Sugar (BS)")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader("Risk Level Distribution")
fig3 = px.pie(filtered, names="RiskLevel",
              color="RiskLevel",
              color_discrete_map={"low risk": "#2dc653", "mid risk": "#f4a261", "high risk": "#c0392b"},
              title="Proportion of Risk Levels")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

st.subheader("Patient Records")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
