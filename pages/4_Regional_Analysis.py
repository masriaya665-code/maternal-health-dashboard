import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Regional Analysis", layout="wide")
BASE = "."

@st.cache_data
def load_who():
    return pd.read_excel(BASE + "/data/who_mmr.xlsx", sheet_name="Data")

who = load_who()
st.title("Regional and Income Group Analysis")
selected_year = st.slider("Select Year", int(who["Year"].min()), int(who["Year"].max()), 2023)
filtered = who[who["Year"] == selected_year]
st.markdown("---")

st.subheader("Average MMR by WHO Region")
region_avg = filtered.groupby("WHO region")["Value Numeric"].mean().reset_index()
region_avg.columns = ["WHO Region", "Average MMR"]
region_avg = region_avg.sort_values("Average MMR", ascending=False)
fig1 = px.bar(region_avg, x="WHO Region", y="Average MMR",
              color="Average MMR", color_continuous_scale="RdPu",
              title=f"Average MMR by WHO Region ({selected_year})")
fig1.update_layout(yaxis_title="MMR (per 100,000 live births)")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")

st.subheader("MMR Distribution by Income Group")
pink_colors = ["#f48fb1", "#f8bbd0", "#e91e8c", "#fce4ec"]
fig2 = px.box(filtered, x="World bank income group", y="Value Numeric",
              color="World bank income group",
              color_discrete_sequence=pink_colors,
              title=f"MMR Distribution by Income Group ({selected_year})",
              labels={"Value Numeric": "MMR (per 100,000 live births)",
                      "World bank income group": "Income Group"})
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")

st.subheader("MMR Trend by WHO Region Over Time")
pink_sequence = ["#e91e8c", "#f48fb1", "#c2185b", "#2dc653", "#f4a261", "#c0392b"]
region_trend = who.groupby(["Year", "WHO region"])["Value Numeric"].mean().reset_index()
fig3 = px.line(region_trend, x="Year", y="Value Numeric", color="WHO region",
               title="MMR Trend by WHO Region (1985-2023)")
fig3.update_layout(yaxis_title="MMR (per 100,000 live births)")
st.plotly_chart(fig3, use_container_width=True)
