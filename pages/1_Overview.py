import streamlit as st
import pandas as pd

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

BASE = "/content/drive/My Drive/maternal_health_dashboard"

@st.cache_data
def load_who():
    return pd.read_excel(BASE + "/data/who_mmr.xlsx.xlsx", sheet_name="Data")

who = load_who()

st.title("📊 Global Maternal Mortality — Overview")
st.markdown("Key statistics from WHO data (1985–2023)")

# --- KPI CARDS ---
latest = who[who["Year"] == who["Year"].max()]
earliest = who[who["Year"] == who["Year"].min()]

latest_avg = latest["Value Numeric"].mean()
earliest_avg = earliest["Value Numeric"].mean()
pct_change = ((latest_avg - earliest_avg) / earliest_avg) * 100

highest = latest.loc[latest["Value Numeric"].idxmax()]
lowest = latest[latest["Value Numeric"] > 0].loc[latest[latest["Value Numeric"] > 0]["Value Numeric"].idxmin()]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌍 Global Avg MMR (2023)", f"{latest_avg:.0f}", "per 100k live births")
col2.metric("📉 Reduction since 1985", f"{abs(pct_change):.1f}%", "improvement")
col3.metric("🔴 Highest MMR (2023)", f"{highest['Value Numeric']:.0f}", highest["Country"])
col4.metric("🟢 Lowest MMR (2023)", f"{lowest['Value Numeric']:.1f}", lowest["Country"])

st.markdown("---")

# --- TABLE: Top 10 highest MMR countries in 2023 ---
st.subheader("🔴 Top 10 Countries with Highest Maternal Mortality (2023)")
top10 = latest.nlargest(10, "Value Numeric")[["Country", "WHO region", "World bank income group", "Value Numeric"]]
top10.columns = ["Country", "WHO Region", "Income Group", "MMR (per 100k)"]
top10["MMR (per 100k)"] = top10["MMR (per 100k)"].round(0).astype(int)
st.dataframe(top10, use_container_width=True)
