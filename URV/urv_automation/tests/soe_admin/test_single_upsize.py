import os
import pytest
from urv_automation.soe_admin import CliInputSpec


rpt_db_name = 'Test_Reporting'
staging_db_name = 'Test_Staging'

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("create_rpt_cfg_db",
                                     "remove_soeadmin_logs")


def test_full_upsize_successful(configuration_name,
                                create_rpt_db,
                                upsize_and_populate_db):
    """
    This test is testing if the SoeAdmin with isam_to_sql parameter succeeds
    and if the expected logs are written into logfiles

    """
    # Create rpt and staging dbs
    create_rpt_db(rpt_db_name, staging_db_name)
    # Fill reporting and staging databases with data
    upsize_and_populate_db(configuration_name, rpt_db_name, staging_db_name,
                           isam_to_sql=True)
    # Parse logfiles
    log_files_dir = os.path.dirname(CliInputSpec.tool_executable)
    parse_sum_path = os.path.join(log_files_dir,
                                  'LogConfigParseSummary.html')
    details_log_path = os.path.join(log_files_dir,
                                    f"{configuration_name}Log.html")
    assert os.path.exists(parse_sum_path)
    assert os.path.exists(details_log_path)
    with open(parse_sum_path) as f:
        assert f'Database conversion succeeded {configuration_name}' in \
               f.read()
    with open(details_log_path) as f:
        assert 'Upsize finished' in f.read()


def test_reporting_population_successful(configuration_name,
                                         create_rpt_db,
                                         upsize_and_populate_db):
    """
    This test is testing if the SoeAdmin command with isam_to_sql and
    reporting_db_population parameters succeeds and
    if the expected logs are written into logfiles

    """
    # Create rpt and staging dbs
    create_rpt_db(rpt_db_name, staging_db_name)
    # Fill reporting and staging databases with data
    upsize_and_populate_db(configuration_name, rpt_db_name, staging_db_name,
                           isam_to_sql=True, rpt_db_population=True)
    # Parse logfiles
    log_files_dir = os.path.dirname(CliInputSpec.tool_executable)
    parse_sum_path = os.path.join(log_files_dir,
                                  'LogConfigParseSummary.html')
    details_log_path = os.path.join(log_files_dir,
                                    f"{configuration_name}Log.html")
    assert os.path.exists(parse_sum_path)
    assert os.path.exists(details_log_path)
    with open(parse_sum_path) as file:
        assert 'Database conversion succeeded {}'.format(configuration_name) \
               in file.read()
    with open(details_log_path) as file:
        data = file.read()
        assert 'Upsize finished' in data
        assert f"Starting reporting database population - reporting DB: " \
               f"{rpt_db_name}" in data
        assert "Reporting database population completed successfully" in data
