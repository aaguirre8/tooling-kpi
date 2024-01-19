import os

from dotenv import load_dotenv
import pandas as pd

from src.database.DatabaseManager import DatabaseManager
from src.etl import constants
from src.etl import data_model
from src.etl import utils
from src.Logger import Logger


def main():

    logger_manager = Logger("etl")
    logger = logger_manager.get_logger()

    load_dotenv()
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    tooling_db = os.getenv("TOOLING_DB")
    schema = os.getenv("SCHEMA")
    output_table = os.getenv("COMPLETED_WORK_ORDERS_TABLE")

    # Extract data from source
    df = pd.read_excel(
        "notebooks/Tooling Dashboard - TAM5.xlsx", skiprows=1, date_format="Modified Date"
    )

    logger.info(f"Extracted data from source - {df.head(5)}")

    # Define schema
    df = df.rename(columns=constants.RENAMED_COL_NAMES)

    # Transform data
    df = utils.transform_data_to_scd(df)
    df = utils.add_tracking_data(df)

    # Rearrange columns
    df = df[constants.REARRANGED_COL_NAMES]

    # Add ColumnsDefinition
    df = df.astype(data_model.data_model)

    logger.info(f"Transformed data - {df.head(5)}")

    # Load data to database
    db_manager = DatabaseManager(user, password, host, port, tooling_db, logger)
    db_manager.insert_data(df, output_table)
    
    logger.info(f"Loaded data to {tooling_db}.{schema}.{output_table}")


if __name__ == "__main__":
    main()
