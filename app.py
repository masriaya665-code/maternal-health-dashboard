import streamlit as st

st.set_page_config(page_title="Maternal Health Dashboard", page_icon="🤱", layout="wide")

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🤱 Maternal Health Analytics Dashboard")
        st.subheader("Please enter the password to continue")
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
    st.title("🤱 Welcome to the Maternal Health Analytics Dashboard")
    st.markdown("""
    Use the **sidebar** to navigate between pages:
    
    - 📊 **Overview** — Global KPIs and key statistics
    - 📈 **Global Trends** — MMR trends over time
    - 🗺️ **Geographic Map** — World map of maternal mortality
    - 📦 **Regional Analysis** — Breakdown by region and income group
    - 🧑‍⚕️ **Patient Explorer** — Explore individual patient data
    - 🤖 **Risk Predictor** — Predict maternal risk level (ML model)
    """)
