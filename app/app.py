from st_pages import show_pages_from_config
import streamlit as st


# Initialize the app
st.set_page_config(
    page_title="Tooling KPI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)
show_pages_from_config()

# App title
st.markdown("""
<style>
    .tooling-kpi-dashboard-title {
        color: #153D64;
        font-size: 48px;
        font-family: font-family: 'Roboto', sans-serif;; 
    }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="tooling-kpi-dashboard-title">Tooling KPI Dashboard</div>', unsafe_allow_html=True)


