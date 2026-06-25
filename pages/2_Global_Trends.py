import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Trends", layout="wide")
BASE = "."

@st.cache_data
def load_who():
    return pd.read_excel(BASE + "/data/who_mmr.xlsx", sheet_name="Data")

who = load_who()
st.title("Maternal Mortality Trends Over Time")

st.subheader("Global Average MMR (1985-2023)")
global_trend = who.groupby("Year")["Value Numeric"].mean().reset_index()
global_trend.columns = ["Year", "Average MMR"]
fig1 = px.line(global_trend, x="Year", y="Average MMR", title="Global Average Maternal Mortality Ratio", markers=True, color_discrete_sequence=["#c0392b"])
fig1.update_layout(yaxis_title="MMR (per 100,000 live births)")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")

st.subheader("Country Comparison")
countries = sorted(who["Country"].unique().tolist())
selected = st.multiselect("Select countries to compare:", countries, default=["Lebanon", "France", "Afghanistan", "Nigeria"])
if selected:
    filtered = who[who["Country"].isin(selected)]
    fig2 = px.line(filtered, x="Year", y="Value Numeric", color="Country", title="Maternal Mortality Ratio by Country", markers=True)
    fig2.update_layout(yaxis_title="MMR (per 100,000 live births)")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Please select at least one country.")
st.markdown("---")

st.subheader("Trend by World Bank Income Group")
income_trend = who.groupby(["Year", "World bank income group"])["Value Numeric"].mean().reset_index()
fig3 = px.line(income_trend, x="Year", y="Value Numeric", color="World bank income group", title="Maternal Mortality Ratio by Income Group", markers=False)
fig3.update_layout(yaxis_title="MMR (per 100,000 live births)")
st.plotly_chart(fig3, use_container_width=True)
