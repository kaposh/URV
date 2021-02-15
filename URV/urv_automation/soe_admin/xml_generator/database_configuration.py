"""Single configuration of XML config file."""
from urv_automation.soe_admin.xml_generator import DatabaseParameters
from urv_automation.soe_admin.xml_generator import PhaseParameters


class DatabaseConfiguration:
    """
    Configuration of the xml config file used by SoeAdmin to upsize the SQL DB.

    ...

    Attributes
    ----------
    configuration_name:
        Returns name of configuration
    database_parameters:
        Returns database parameters
    phase_parameters:
        Returns phase parameters

    """

    def __init__(self, config_name):
        self._config_name = config_name
        self._database_parameters = DatabaseParameters()
        self._phase_parameters = PhaseParameters()

    @property
    def configuration_name(self):
        """
        Name of database configuration.

        Returns
        -------
        str
            Returns a name of database configuration

        """
        return self._config_name

    @property
    def database_parameters(self):
        """
        Database parameters.

        Returns
        -------
        DatabaseParameters
            Returns a data object with database parameters

        """
        return self._database_parameters

    @property
    def phase_parameters(self):
        """
        Phase parameters.

        Returns
        -------
        PhaseParameters
            Returns a data object with phase parameters

        """
        return self._phase_parameters
