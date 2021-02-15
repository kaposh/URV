from subprocess import CalledProcessError

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation.sqlserver import RptCfgDbQueries
from urv_automation.urv import CliInputSpec


reporting_db_name = "Test_Reporting"
staging_db_name = "Test_Staging"
# will be read by delete_used_database fixture
used_databases = [reporting_db_name, staging_db_name]

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("delete_used_database",
                                     "create_rpt_cfg_db")


def test_create_rpt_db_successful():
    """
    This test is testing if the CREATE_RPT_DB command successfully runs and
    the reporting and staging databases are created

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="CREATE_RPT_DB",
                                  reporting_config_db_server="localhost",
                                  reporting_db_server="localhost",
                                  reporting_db_name=reporting_db_name,
                                  staging_db_name=staging_db_name)

    cr.load_input_spec(urv_input_spec)
    cr.run_command()
    sql_db_queries = RptCfgDbQueries()
    assert "Test_Reporting" in sql_db_queries.get_all_rpt_db_names()
    assert "Test_Staging" in sql_db_queries.get_all_staging_db_names()


def test_create_rpt_db_missing_staging_param():
    """
    This test is testing if the CREATE_RPT_DB fails due to missing staging
    parameter in the command

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="CREATE_RPT_DB",
                                  reporting_config_db_server="localhost",
                                  reporting_db_server="localhost",
                                  reporting_db_name=reporting_db_name)
    cr.load_input_spec(urv_input_spec)
    with pytest.raises(CalledProcessError):
        cr.run_command()


def test_create_rpt_db_missing_reporting_param():
    """
    This test is testing if the CREATE_RPT_DB fails due to missing reporting
    parameter in the command

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="CREATE_RPT_DB",
                                  reporting_config_db_server="localhost",
                                  reporting_db_server="localhost",
                                  staging_db_name=staging_db_name)
    cr.load_input_spec(urv_input_spec)
    with pytest.raises(CalledProcessError):
        cr.run_command()
