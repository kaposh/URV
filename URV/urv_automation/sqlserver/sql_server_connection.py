"""Connections to SQL server."""
import pyodbc

from urv_automation.sqlserver import Rows


class SqlServerConnection:
    """
    Connect to SQL server and run queries or statement.

    ...

    Attributes
    ----------
    server_name : str
        Name of server where SQL server is running
    database_name : str
        Name of database for establishing the connection

    ...

    Methods
    -------
    run_query(query):
        Runs the SQL query on established connection and return Rows object
    run_statement(statement):
        Runs the SQL statement on established connection
    """

    def __enter__(self):
        """Create a connection to SQL database."""
        self.connection = pyodbc.connect(self.connection_config)
        self.connection.autocommit = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: U100
        """Close the connection."""
        self.connection.close()

    def __init__(self, server_name, database_name=None):
        self.connection_config = "Driver={SQL Server};" \
                                 f"Server={server_name};" \
                                 "Trusted_Connection=yes;"
        if database_name:
            self.connection_config += "DATABASE={};".format(database_name)

    def run_query(self, sql_query):
        """
        Run the SQL query.

        Parameters
        ----------
        sql_query : str
            SQL query to be run

        Returns
        -------
        Rows
            Returns the output of SQL query

        """
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        return Rows(cursor.fetchall())

    def run_statement(self, statement):
        """
        Run the SQL statement.

        Parameters
        ----------
        statement : str
            SQL statement to be run

        """
        cursor = self.connection.cursor()
        cursor.execute(statement)
