"""SQL server queries."""
from urv_automation.sqlserver import SqlServerConnection


class SqlSystemQueries:
    """
    Helper class for running SQL queries over system db.

    ...

    Attributes
    ----------
    server_name : str
        Server where the SQL server is running

    ...

    Methods
    -------
    delete_database_if_exists(database_name):
        Deletes the SQL database if it exists
    does_db_exist(database_name):
        Find out if the SQL DB exists and return the value
    """

    def __init__(self, server_name="localhost"):
        self.server_name = server_name

    def delete_database(self, database_name):
        """
        Delete the SQL database if it exists.

        Parameters
        ----------
        database_name : str
            Database name to be deleted

        """
        if self.does_db_exist(database_name):
            with SqlServerConnection(
                    server_name=self.server_name) as connection:
                connection.run_statement("ALTER DATABASE {} SET single_user "
                                         "with rollback immediate"
                                         .format(database_name))
                connection.run_statement("DROP DATABASE {}"
                                         .format(database_name))

    def does_db_exist(self, database_name):
        """
        Delete the SQL database if it exists.

        Parameters
        ----------
        database_name : str
            Database name to be deleted

        Returns
        -------
        bool
            If SQL database exists return True, otherwise False

        """
        with SqlServerConnection(server_name=self.server_name) as connection:
            databases = connection.run_query(
                f"SELECT name FROM sys.databases WHERE name='{database_name}'")
        return databases.row_count > 0
