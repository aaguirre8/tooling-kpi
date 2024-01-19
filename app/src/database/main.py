import os

from dotenv import load_dotenv
from src.database.DatabaseManager import DatabaseManager
from src.database import table_queries
from src.Logger import Logger


def main():
    """
    Main entry point of the application.

    This function initializes a PostgreSQL database and creates tables.
    It loads database credentials from environment variables using `dotenv`.

    Raises:
        Any exceptions that occur during database initialization or table creation.
    """

    logger_manager = Logger("database_setup")
    logger = logger_manager.get_logger()

    load_dotenv()
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    tooling_db = os.getenv("TOOLING_DB")

    # Create a database manager object
    db_manager = DatabaseManager(user, password, host, port, tooling_db, logger)

    # Create database
    # with context block is not used here
    # CREATE DATABASE cannot run inside a transaction block
    # Refer to https://www.postgresql.org/docs/9.1/sql-createdatabase.html for more information
    default_conn = db_manager.create_default_connection()
    db_manager.create_database(default_conn)

    # Create tables
    conn = db_manager.create_connection()
    with conn as con:
        db_manager.create_tables(table_queries.CREATE_COMPLETED_WORK_ORDERS_TABLE, con)


if __name__ == "__main__":
    main()
