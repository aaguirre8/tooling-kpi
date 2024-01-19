import os

from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
from st_pages import show_pages_from_config
import streamlit as st

from src.database.DatabaseManager import DatabaseManager as api_DatabaseManager
from src.database import sql_queries
from src.Logger import Logger


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


logger_manager = Logger("app")
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

if conn is not None:

    with conn as con:
        df = pd.read_sql(sql_queries.COMPLETED_WORK_ORDERS_QUERY, con)

    if df.empty:
        pass

    else:

        order_counts = df.groupby(['technician', 'status']).size().unstack(fill_value=0).reset_index()

        # Assuming 'order_counts' is your DataFrame after processing
        fig = px.bar(order_counts, x='technician', y=['Finished', 'WIP'], 
                    title='Orders by Technician',
                    labels={'value': 'Number of Orders', 'variable': 'Order Status'},
                    barmode='group')

        # Enhancing the plot aesthetics
        fig.update_layout(xaxis_title='Technician',
                        yaxis_title='Number of Orders',
                        legend_title='Order Status',
                        plot_bgcolor='white',
                        showlegend=True)

        st.plotly_chart(fig, use_container_width=True)

else: 
    pass




