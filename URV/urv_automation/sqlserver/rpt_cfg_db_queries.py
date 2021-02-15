"""SQL queries on the reporting config database."""
from urv_automation.sqlserver import SqlServerConnection


class RptCfgDbQueries:
    """
    Helper class for running SQL queries over reporting config database.

    ...

    Attributes
    ----------
    rpt_cfg_db_name : str
        Name of reporting config database
    server_name : str
        Server where the SQL server is running

    ...

    Methods
    -------
    get_all_rpt_db_names():
        Gets a list of existing reporting databases names
    get_all_staging_db_names():
        Gets a list of existing staging databases names
    """

    def __init__(self, rpt_cfg_db_name="SOEI_ReportingConfig",
                 server_name="localhost"):
        self.rpt_cfg_db_name = rpt_cfg_db_name
        self.server_name = server_name

    def get_all_rpt_db_names(self):
        """
        Get a list of existing reporting databases names.

        Returns
        -------
        list
            List of existing reporting database names

        """
        with SqlServerConnection(self.server_name, self.rpt_cfg_db_name) \
                as connection:
            databases = connection.run_query(
                "SELECT reportingDbName FROM SOEI_ReportingDatabases ;")
        return databases["reportingDbName"]

    def get_all_staging_db_names(self):
        """
        Get a list of existing staging databases names.

        Returns
        -------
        list
            List of existing staging database names

        """
        with SqlServerConnection(self.server_name, self.rpt_cfg_db_name) \
                as connection:
            databases = connection.run_query(
                "SELECT stagingDbName FROM SOEI_ReportingDatabases ;")
        return databases["stagingDbName"]
