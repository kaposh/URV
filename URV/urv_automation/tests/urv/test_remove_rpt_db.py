from subprocess import CalledProcessError

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation.sqlserver import SqlServerConnection, SqlSystemQueries
from urv_automation.urv import CliInputSpec


reporting_db_name = "Test_Reporting"
staging_db_name = "Test_Staging"
# will be read by delete_used_database fixture
used_databases = [reporting_db_name,
                  staging_db_name]

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("delete_used_database",
                                     "create_rpt_cfg_db")


def test_remove_rpt_db_successful(create_rpt_db):
    """
    This test is testing if the REMOVE_RPT_DB command successfully runs
    and the reporting and config databases are successfully removed

    """
    # Create test dbs
    create_rpt_db(reporting_db_name, staging_db_name)

    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="REMOVE_RPT_DB",
                                  reporting_config_db_server="localhost",
                                  reporting_db_server="localhost",
                                  reporting_db_name=reporting_db_name)
    cr = CommandRunner()
    cr.load_input_spec(input_spec=urv_input_spec)
    cr.run_command()
    sql_queries = SqlSystemQueries()
    assert sql_queries.does_db_exist(reporting_db_name) is False
    assert sql_queries.does_db_exist(staging_db_name) is False


def test_remove_rpt_db_not_required_staging_db_param(create_rpt_db):
    """
    This test is testing if the REMOVE_RPT_DB command fails
    if unexpected parameter staging_db_name is set

    """
    # Create test dbs
    create_rpt_db(reporting_db_name, staging_db_name)

    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="REMOVE_RPT_DB",
                                  reporting_config_db_server="localhost",
                                  reporting_db_server="localhost",
                                  reporting_db_name=reporting_db_name,
                                  staging_db_name=staging_db_name)
    cr = CommandRunner()
    cr.load_input_spec(input_spec=urv_input_spec)
    with pytest.raises(CalledProcessError):
        cr.run_command()
