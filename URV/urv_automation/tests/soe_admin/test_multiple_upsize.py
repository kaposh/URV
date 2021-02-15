import os

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation import settings
from urv_automation.soe_admin import CliInputSpec as SoeAdminInputSpec
from urv_automation.soe_admin.xml_generator import DatabaseConfiguration, XmlGenerator
from urv_automation.test_data import urv_testdata

rpt_db_name = 'Test_Reporting'
staging_db_name = 'Test_Staging'

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("create_rpt_cfg_db",
                                     "remove_soeadmin_logs")


def test_full_upsize_multiple_dbs_successful(configuration_name,
                                             create_rpt_db,
                                             ):
    """
    Run SoeAdmin and upsize one the configuration defined in configuration_name
    out of all existing configurations exported in xml config

    Parameters
    ----------
    configuration_name : str
        Name of DB configuration to be run in this test

    """
    # Create rpt and staging dbs
    create_rpt_db(rpt_db_name, staging_db_name)
    # Generate XML file with all available configurations
    xml_generator = XmlGenerator()
    for configuration in list(urv_testdata.get_available_dbs_info()):
        db_config = DatabaseConfiguration(configuration)
        db_config.database_parameters.ISAMDB = configuration_name
        db_config.database_parameters.ISAMDBLocation = \
            urv_testdata.get_isam_db_folder(configuration_name)
        db_config.database_parameters.SQLUpsizedDB = 'Test_Staging'
        db_config.database_parameters.SQLReportingDB = 'Test_Reporting'
        db_config.phase_parameters.ISAMToSQL = 'on'
        xml_generator.add_database_configuration(db_config)
    xml_generator.generate(settings.SOE_ADMIN_DEFAULT_CONFIG_FILE)
    # Run SOE Admin
    cr = CommandRunner()
    urv_input_spec = SoeAdminInputSpec()
    urv_input_spec.set_parameters(xml_config_file=
                                  settings.SOE_ADMIN_DEFAULT_CONFIG_FILE,
                                  data_set=configuration_name)

    cr.load_input_spec(urv_input_spec)
    cr.run_command()
    parse_summary_log_path = os.path.join(os.path.dirname(urv_input_spec.tool_executable),
                                          'LogConfigParseSummary.html')
    upsize_details_log_path = os.path.join(os.path.dirname(urv_input_spec.tool_executable),
                                           "{}Log.html"
                                           .format(configuration_name))
    assert os.path.exists(parse_summary_log_path)
    assert os.path.exists(upsize_details_log_path)
    with open(parse_summary_log_path) as f:
        assert 'Database conversion succeeded {}'.format(configuration_name)\
               in f.read()
    with open(upsize_details_log_path) as f:
        assert 'Upsize finished' in f.read()
