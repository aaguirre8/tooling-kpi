import os
from io import StringIO

from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from src.database.DatabaseManager import DatabaseManager as api_DatabaseManager
from src.database import sql_queries
from src.etl.etl import main as api_update_metrics


# Session states
st.session_state["ss_uploaded_file"] = False

# Subheader
st.markdown("""
<style>
    .update-metrics-subheader {
        color: #153D64;
        font-size: 36px;
        font-family: font-family: 'Roboto', sans-serif;; 
    }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="update-metrics-subheader">Update Metrics</div>', unsafe_allow_html=True)

# Spacing
st.markdown("""
<style>
    .custom-spacing {
        margin-bottom: 20px; /* Adjust the margin as needed for spacing */
    }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="custom-spacing"></div>', unsafe_allow_html=True)

# Screen
tab1, tab2, tab3, tab4 = st.tabs(["Upload File", "-", "-", "Preview Data"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            # Text
            st.markdown("""
            <style>
                .text {
                    color: #153D64;
                    font-size: 24px;
                    font-family: font-family: 'Roboto', sans-serif;; 
                }
            </style>
            """, unsafe_allow_html=True)
            st.markdown('<div class="text">Upload file</div>', unsafe_allow_html=True)

            uploaded_file = st.file_uploader("", type=["xlsx"])

            if uploaded_file is not None:
                uploaded_data = pd.read_excel(uploaded_file)
                st.session_state["ss_uploaded_file"] = True

            if st.session_state["ss_uploaded_file"]:
                start_button = st.button("Update metrics")
                if start_button:
                    api_update_metrics(uploaded_data)
                    
                    # Custom text
                    st.markdown("""
                    <style>
                        .custom-text {
                            color: #153D64;
                            font-size: 18px;
                            font-family: font-family: 'Roboto', sans-serif;; 
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="custom-text">Succesfully updated metrics</div>', unsafe_allow_html=True)

with tab4:
    from src.Logger import Logger

    logger_manager = Logger("preview_data")
    logger = logger_manager.get_logger()

    load_dotenv()
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    tooling_db = os.getenv("TOOLING_DB")
    schema = os.getenv("SCHEMA")
    input_table = os.getenv("COMPLETED_WORK_ORDERS_TABLE")

    db_manager = api_DatabaseManager(user, password, host, port, tooling_db, logger)
    conn = db_manager.create_connection()

    with conn as con:
        df = pd.read_sql(sql_queries.COMPLETED_WORK_ORDERS_QUERY, con)
        column_mapping = {col: col.replace("_", " ").title() for col in df.columns}
        df = df.rename(columns=column_mapping)
        
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True)
    
# Custom tabs text
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #153D64;
        font-size: 18px;
        font-family: 'Roboto', sans-serif;
    }
</style>
""", unsafe_allow_html=True)