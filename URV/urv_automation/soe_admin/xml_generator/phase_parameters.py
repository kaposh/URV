"""Phase parameters of the Soe Admin XML configuration section."""
from dataclasses import dataclass

from urv_automation.soe_admin.xml_generator import ParametersBase


@dataclass
class PhaseParameters(ParametersBase):
    """
    Holds the information about the phase parameters.

    ...
    Attributes
    ----------
    ISAMToSQL:
        Upsize the database
    ReportingDBPopulation:
        Fill the reporting database from upsized data
    """

    ISAMToSQL: str = 'off'
    ReportingDBPopulation: str = 'off'
