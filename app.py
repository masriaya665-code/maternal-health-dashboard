import streamlit as st

st.set_page_config(page_title="Maternal Health Dashboard", layout="wide")

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("Maternal Health Analytics Dashboard")
        st.markdown("This dashboard is restricted. Please enter the password to continue.")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "maternalhealth2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        return False
    return True

if check_password():
    st.title("Maternal Health Analytics Dashboard")
    st.markdown("""
    Welcome. Use the sidebar to navigate between sections of the dashboard.

    - **Overview** — Global KPIs and key statistics
    - **Global Trends** — Maternal mortality trends over time
    - **Geographic Map** — World map of maternal mortality by country
    - **Regional Analysis** — Breakdown by WHO region and income group
    - **Patient Explorer** — Explore individual patient clinical data
    - **Risk Predictor** — Predict maternal risk level using a machine learning model
    """)
