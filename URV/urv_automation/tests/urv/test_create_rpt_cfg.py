import os

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation.sqlserver import SqlSystemQueries
from urv_automation.urv import CliInputSpec

# will be read by delete_used_database fixture
used_databases = ["SOEI_ReportingConfig"]

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("delete_used_database")


def test_create_rpt_cfg_successful():
    """
    This test is testing if the CREATE_RPT_CFG command successfully runs and
    the config database is created

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="CREATE_RPT_CFG",
                                  reporting_config_db_server="localhost",
                                 )

    cr.load_input_spec(urv_input_spec)
    cr.run_command()
    sql_queries = SqlSystemQueries()
    assert sql_queries.does_db_exist("SOEI_ReportingConfig") is True


def test_create_rpt_cfg_logfile():
    """
    This test is testing if the logfile exists and contains expected substring
    when CREATE_RPT_CFG is called

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="CREATE_RPT_CFG",
                                  reporting_config_db_server="localhost")
    urv_log_file_path = urv_input_spec.tool_arguments['log_file'].get_value()
    cr.load_input_spec(urv_input_spec)
    cr.run_command()
    assert os.path.exists(urv_log_file_path) is True
    with open(urv_log_file_path) as f:
        assert 'Operation completed successfully' in f.read()
