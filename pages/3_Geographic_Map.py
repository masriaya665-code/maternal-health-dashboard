import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Geographic Map", page_icon="🗺️", layout="wide")

BASE = "/content/drive/My Drive/maternal_health_dashboard"

@st.cache_data
def load_who():
    return pd.read_excel(BASE + "/data/who_mmr.xlsx.xlsx", sheet_name="Data")

who = load_who()

st.title("🗺️ Global Maternal Mortality Map")
st.markdown("Explore how maternal mortality is distributed across the world.")

# --- YEAR SLIDER ---
min_year = int(who["Year"].min())
max_year = int(who["Year"].max())
selected_year = st.slider("Select Year", min_year, max_year, max_year)

# --- FILTER DATA ---
filtered = who[who["Year"] == selected_year]

# --- CHOROPLETH MAP ---
fig = px.choropleth(
    filtered,
    locations="Country ISO 3 code",
    color="Value Numeric",
    hover_name="Country",
    hover_data={"Value Numeric": True, "WHO region": True, "World bank income group": True},
    color_continuous_scale="Reds",
    title=f"Maternal Mortality Ratio by Country ({selected_year})",
    labels={"Value Numeric": "MMR (per 100k live births)"}
)
fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- DATA TABLE BELOW MAP ---
st.subheader(f"📋 Data Table — {selected_year}")
table = filtered[["Country", "WHO region", "World bank income group", "Value Numeric"]].copy()
table.columns = ["Country", "WHO Region", "Income Group", "MMR (per 100k)"]
table = table.sort_values("MMR (per 100k)", ascending=False).reset_index(drop=True)
table["MMR (per 100k)"] = table["MMR (per 100k)"].round(1)
st.dataframe(table, use_container_width=True)
