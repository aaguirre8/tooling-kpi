import logging

import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine


class DatabaseManager:
    """
    A class to manage PostgreSQL database operations.

    Attributes:
        _user (str): Database user name.
        _password (str): Database password.
        _host (str): Database host address.
        _port (int): Database port number.
        _db_name (str): Name of the database to manage.
    """

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        db_name: str,
        logger: logging.Logger
    ) -> None:
        
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._db_name = db_name
        self.logger = logger

    def create_database(self, con: psycopg2.connect) -> None:
        """
        Creates a new database with the name specified in the class instance.

        This method avoids using f-strings or direct string interpolation to construct the SQL query.
        Instead, it uses psycopg2's sql.SQL() and sql.Identifier() to securely inject the database name,
        preventing SQL injection vulnerabilities.

        Args:
            con (psycopg2.connect): Connection object to the default PostgreSQL database.

        Raises:
            Exception: If the database creation fails.
        """
        logger = self.logger
        try:
            with con.cursor() as cursor:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self._db_name)))
        except Exception as e:
            logger.error(f"Error creating database: {e}")

    def create_tables(self, sql_query: str, conn: psycopg2.connect) -> None:
        """
        Executes a SQL query to create tables in the database.

        Args:
            sql_query (str): SQL query for creating tables.
            conn (psycopg2.connect): Connection object to the database.

        Raises:
            Exception: If the table creation fails.
        """
        logger = self.logger
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
        except Exception as e:
            logger.error(f"Error creating tables: {e}")

    def insert_data(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Inserts data from a pandas DataFrame into a specified database table.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to insert.
            table_name (str): The name of the table in which to insert the data.

        Raises:
            Exception: If the data insertion fails.
        """
        logger = self.logger
        try:

            # Create an SQLAlchemy engine for the specified database
            # The SQLAlchemy engine is used by pandas' to_sql method to insert data into the database
            engine = create_engine(
                f"postgresql://{self._user}:{self._password}@{self._host}:{self._port}/{self._db_name}"
            )

            # The reason for not using the context manager is that the SQLAlchemy engine
            # is not compatible with it. The engine is closed after the context manager exits,
            # which prevents pandas from inserting data into the database.
            df.to_sql(
                table_name,
                engine,
                if_exists="append",
                index=False,
                method="multi"
                )
            
            engine.dispose()
            
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")

    def create_default_connection(self) -> psycopg2.connect:
        """
        Creates a connection engine to the default PostgreSQL database.

        This method is typically used for initial operations like creating a new database.

        Returns:
            psycopg2.connect: A connection object to the default database.

        Raises:
            Exception: If the connection engine creation fails.
        """
        logger = self.logger
        try:

            conn = psycopg2.connect(
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                dbname="postgres",
            )
            conn.autocommit = True

            return conn

        except Exception as e:
            logger.error(f"Error creating connection engine: {e}")

    def create_connection(self) -> psycopg2.connect:
        """
        Creates a connection engine to the specified database.

        This method is used to connect to a database that has already been created.

        Returns:
            psycopg2.connect: A connection object to the specified database.

        Raises:
            Exception: If the connection engine creation fails.
        """
        logger = self.logger
        try:

            conn = psycopg2.connect(
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                dbname=self._db_name,
            )
            conn.autocommit = True

            return conn

        except Exception as e:
            logger.error(f"Error creating connection engine: {e}")
