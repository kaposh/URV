"""Database parameters of the Soe Admin XML configuration section."""
from dataclasses import dataclass

from urv_automation.soe_admin.xml_generator import ParametersBase


@dataclass
class DatabaseParameters(ParametersBase):
    """
    Hold the information about the database configuration parameters.

    ...
    Attributes
    ----------
    ISAMDB:
        Isam database name
    ISAMDBLocation:
        Path to ISAM database
    ISAMServerName:
        Name of server with ISAM database
    SQLServer:
        Name of server with running SQL server
    SQLUpsizedDB:
        Name of empty SQL upsized database
    SQLReportingDB:
        Name of empty SQL reporting database
    UIDCOTMapping:
        Populate duplicate treatment plan mapping’ in EXACT
        under Tools > Other Tools > Populate duplicate treatment plan mapping
    CheckData:
        Check the upsized data against the original data

    Methods
    -------
    load_from_config_file(config_name):
        Loads the data from configuration file into dataclass attributes

    """

    ISAMDB: str = None
    ISAMDBLocation: str = None
    ISAMServerName: str = 'localhost'
    SQLServer: str = 'localhost'
    SQLUpsizedDB: str = None
    SQLReportingDB: str = None
    UIDCOTMapping: bool = True
    CheckData: bool = False
