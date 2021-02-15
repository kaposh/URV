import os

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation.sqlserver import SqlSystemQueries
from urv_automation.urv import CliInputSpec

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("create_rpt_cfg_db")


def test_remove_rpt_cfg_successful():
    """
    This test is testing if the REMOVE_RPT_CFG command successfully runs
    and the config databases is successfully removed

    """
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="REMOVE_RPT_CFG",
                                  reporting_config_db_server="localhost")
    cr = CommandRunner()
    cr.load_input_spec(input_spec=urv_input_spec)
    cr.run_command()
    sql_queries = SqlSystemQueries()
    assert sql_queries.does_db_exist("SOEI_ReportingConfig") is False


def test_remove_rpt_cfg_logfile():
    """
    This test is testing if the logfile exists and contains expected substring
    when REMOVE_RPT_CFG is called

    """
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="REMOVE_RPT_CFG",
                                  reporting_config_db_server="localhost")
    urv_log_file_path = urv_input_spec.tool_arguments['log_file'].get_value()
    cr = CommandRunner()
    cr.load_input_spec(input_spec=urv_input_spec)
    cr.run_command()
    assert os.path.exists(urv_log_file_path) is True
    with open(urv_log_file_path) as f:
        assert 'Removing the reporting configuration database ' \
               'SOEI_ReportingConfig from server localhost' in f.read()
    with open(urv_log_file_path) as f:
        assert 'Operation completed successfully' in f.read()
