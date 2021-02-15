import os

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation.sqlserver import SqlSystemQueries
from urv_automation.urv import CliInputSpec


reporting_db_name_1 = "Test_Reporting_1"
staging_db_name_1 = "Test_Staging_1"
reporting_db_name_2 = "Test_Reporting_2"
staging_db_name_2 = "Test_Staging_2"
# will be read by delete_used_database fixture
used_databases = [reporting_db_name_1,
                  staging_db_name_1,
                  reporting_db_name_2,
                  staging_db_name_2]

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("delete_used_database",
                                     "create_rpt_cfg_db")


def test_remove_all_rpt_dbs_successful(create_rpt_db):
    """
    This test is testing if the REMOVE_ALL_RPT_DBS command successfully runs
    and all reporting and staging databases are successfully removed

    """
    # Create test dbs
    create_rpt_db(reporting_db_name_1, staging_db_name_1)
    create_rpt_db(reporting_db_name_2, staging_db_name_2)

    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="REMOVE_ALL_RPT_DBS",
                                  reporting_config_db_server="localhost")
    cr = CommandRunner()
    cr.load_input_spec(input_spec=urv_input_spec)
    cr.run_command()
    sql_queries = SqlSystemQueries()
    assert sql_queries.does_db_exist(reporting_db_name_1) is False
    assert sql_queries.does_db_exist(staging_db_name_1) is False
    assert sql_queries.does_db_exist(reporting_db_name_2) is False
    assert sql_queries.does_db_exist(staging_db_name_2) is False


def test_remove_all_rpt_dbs_logfile(create_rpt_db):
    """
    This test is testing if the logfile exists and contains expected substring
    when REMOVE_ALL_RPT_DBS is called

    """
    # Create test dbs
    create_rpt_db(reporting_db_name_1, staging_db_name_1)
    create_rpt_db(reporting_db_name_2, staging_db_name_2)
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="REMOVE_ALL_RPT_DBS",
                                  reporting_config_db_server="localhost")
    urv_log_file_path = urv_input_spec.tool_arguments['log_file'].get_value()
    cr = CommandRunner()
    cr.load_input_spec(input_spec=urv_input_spec)
    cr.run_command()
    assert os.path.exists(urv_log_file_path) is True
    with open(urv_log_file_path) as f:
        assert 'Existing reporting & staging databases Test_Reporting_1 ' \
               'Test_Staging_1 on server localhost removed' \
               in f.read()
    with open(urv_log_file_path) as f:
        assert 'Existing reporting & staging databases Test_Reporting_2 ' \
               'Test_Staging_2 on server localhost removed' \
               in f.read()

