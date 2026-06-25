import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Overview", layout="wide")
BASE = "."

@st.cache_data
def load_who():
    return pd.read_excel(BASE + "/data/who_mmr.xlsx", sheet_name="Data")

who = load_who()
st.title("Maternal Health Analytics Dashboard")
st.markdown("Global overview of maternal mortality based on WHO data (1985-2023)")
st.markdown("---")

latest_year = who["Year"].max()
latest = who[who["Year"] == latest_year]
earliest = who[who["Year"] == who["Year"].min()]
latest_avg = latest["Value Numeric"].mean()
earliest_avg = earliest["Value Numeric"].mean()
pct_change = ((latest_avg - earliest_avg) / earliest_avg) * 100
highest = latest.loc[latest["Value Numeric"].idxmax()]
lowest = latest[latest["Value Numeric"] > 0].loc[latest[latest["Value Numeric"] > 0]["Value Numeric"].idxmin()]
total_countries = latest["Country"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("""<div style="background:#f8f9fa;padding:20px;border-radius:10px;text-align:center;border-left:5px solid #c0392b;"><p style="color:#888;font-size:13px;margin:0;">Global Avg MMR (2023)</p><h1 style="color:#c0392b;margin:5px 0;">{:.0f}</h1><p style="color:#888;font-size:12px;margin:0;">per 100,000 live births</p></div>""".format(latest_avg), unsafe_allow_html=True)
with col2:
    st.markdown("""<div style="background:#f8f9fa;padding:20px;border-radius:10px;text-align:center;border-left:5px solid #2dc653;"><p style="color:#888;font-size:13px;margin:0;">Reduction Since 1985</p><h1 style="color:#2dc653;margin:5px 0;">{:.1f}%</h1><p style="color:#888;font-size:12px;margin:0;">global improvement</p></div>""".format(abs(pct_change)), unsafe_allow_html=True)
with col3:
    st.markdown("""<div style="background:#f8f9fa;padding:20px;border-radius:10px;text-align:center;border-left:5px solid #c0392b;"><p style="color:#888;font-size:13px;margin:0;">Highest MMR (2023)</p><h1 style="color:#c0392b;margin:5px 0;">{:.0f}</h1><p style="color:#888;font-size:12px;margin:0;">{}</p></div>""".format(highest["Value Numeric"], highest["Country"]), unsafe_allow_html=True)
with col4:
    st.markdown("""<div style="background:#f8f9fa;padding:20px;border-radius:10px;text-align:center;border-left:5px solid #5b8dd9;"><p style="color:#888;font-size:13px;margin:0;">Lowest MMR (2023)</p><h1 style="color:#5b8dd9;margin:5px 0;">{:.1f}</h1><p style="color:#888;font-size:12px;margin:0;">{}</p></div>""".format(lowest["Value Numeric"], lowest["Country"]), unsafe_allow_html=True)
with col5:
    st.markdown("""<div style="background:#f8f9fa;padding:20px;border-radius:10px;text-align:center;border-left:5px solid #f4a261;"><p style="color:#888;font-size:13px;margin:0;">Countries Tracked</p><h1 style="color:#f4a261;margin:5px 0;">{}</h1><p style="color:#888;font-size:12px;margin:0;">worldwide</p></div>""".format(total_countries), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

SEQ = ["#2dc653", "#f4a261", "#c0392b", "#5b8dd9", "#a259c4", "#f7c59f"]

col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Top 10 Countries by MMR (2023)")
    top10 = latest.nlargest(10, "Value Numeric")[["Country", "Value Numeric"]].copy()
    top10.columns = ["Country", "MMR"]
    top10 = top10.sort_values("MMR")
    fig1 = px.bar(top10, x="MMR", y="Country", orientation="h",
                  color="Country", color_discrete_sequence=SEQ,
                  labels={"MMR": "MMR (per 100k)"})
    fig1.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig1, use_container_width=True)
with col_right:
    st.subheader("MMR by Income Group (2023)")
    income = latest.groupby("World bank income group")["Value Numeric"].mean().reset_index()
    income.columns = ["Income Group", "Average MMR"]
    income = income.sort_values("Average MMR", ascending=False)
    fig2 = px.bar(income, x="Income Group", y="Average MMR",
                  color="Income Group", color_discrete_sequence=SEQ,
                  labels={"Average MMR": "Avg MMR (per 100k)"})
    fig2.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("Global Trend (1985-2023)")
global_trend = who.groupby("Year")["Value Numeric"].mean().reset_index()
global_trend.columns = ["Year", "Average MMR"]
fig3 = px.area(global_trend, x="Year", y="Average MMR",
               color_discrete_sequence=["#c0392b"],
               labels={"Average MMR": "Avg MMR (per 100,000 live births)"})
fig3.update_traces(fillcolor="rgba(192,57,43,0.15)")
fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0))
st.plotly_chart(fig3, use_container_width=True)
