import os
import pytest
import shutil

from urv_automation.cli_interface import CommandRunner
from urv_automation.soe_admin import CliInputSpec as SoeAdminInputSpec
from urv_automation.urv import CliInputSpec as UrvCliInputSpec
from urv_automation import settings
from urv_automation.soe_admin.xml_generator import DatabaseConfiguration, XmlGenerator
from urv_automation.sqlserver import SqlSystemQueries
from urv_automation.test_data import urv_testdata


def pytest_addoption(parser):
    """
    Defines the command line parameters for pytest

    Parameters
    ----------
    parser
        This is set automatically

    """
    parser.addoption(
        "--test_scope",
        action="store",
        default="all",
        choices=["single", "all"],
        help="Scope of test configurations: all or single",
    )
    parser.addoption(
        "--configuration_name",
        action="store",
        default="",
        help="Name of configuration to be run",
    )


def pytest_generate_tests(metafunc):
    """
    Generate tests based on the number of configuration defined in pytest
    argument.

    Parameters
    ----------
    metafunc
        This is set automatically

    """
    if "configuration_name" in metafunc.fixturenames:
        test_scope = metafunc.config.getoption("test_scope")
        if test_scope == "single":
            configuration_names = [metafunc.config.getoption
                                   ("configuration_name")]
        else:
            configuration_names = list(urv_testdata.get_available_dbs_info())
        metafunc.parametrize("configuration_name", configuration_names)


@pytest.fixture(scope="session", autouse=True)
def recreate_compare_logs_dir():
    # Recreate COMPARE_LOGS_DIR before the session starts
    if os.path.exists(settings.COMPARE_LOGS_DIR):
        shutil.rmtree(settings.COMPARE_LOGS_DIR)
    os.makedirs(settings.COMPARE_LOGS_DIR)


@pytest.fixture(scope="module", autouse=True)
def recreate_urv_logs_dir():
    # Recreate URV_LOGS_DIR before the session starts
    if os.path.exists(settings.URV_LOGS_DIR):
        shutil.rmtree(settings.URV_LOGS_DIR)
    os.makedirs(settings.URV_LOGS_DIR)


@pytest.fixture()
def remove_soeadmin_logs():
    # Recreate URV_LOGS_DIR before the session starts
    log_dir = os.path.dirname(SoeAdminInputSpec.tool_executable)
    all_files = os.listdir(log_dir)
    for file in all_files:
        if file.endswith(".html"):
            os.remove(os.path.join(log_dir, file))


@pytest.fixture()
def create_target_snapshots_dir():
    target_dir = urv_testdata.get_sql_snapshots_target_dir()
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


@pytest.fixture()
def delete_used_database(request):
    def _delete_used_database(db_list):
        for database_name in db_list:
            sql_queries = SqlSystemQueries()
            sql_queries.delete_database(database_name)
    _delete_used_database(getattr(request.module, "used_databases"))
    yield
    _delete_used_database(getattr(request.module, "used_databases"))


@pytest.fixture()
def create_rpt_cfg_db():
    # remove DB if it exists
    sql_queries = SqlSystemQueries()
    sql_queries.delete_database("SOEI_ReportingConfig")

    # create a new config DB
    cr = CommandRunner()
    urv_input_spec = UrvCliInputSpec()
    urv_input_spec.set_parameters(action="CREATE_RPT_CFG",
                                  reporting_config_db_server="localhost")
    cr.load_input_spec(urv_input_spec)
    cr.run_command()
    yield
    sql_queries.delete_database("SOEI_ReportingConfig")


@pytest.fixture
def create_rpt_db():
    created_databases = []
    sql_queries = SqlSystemQueries()

    def _create_rpt_db(rpt_db_name, staging_db_name):
        # remove DBs if they exist
        sql_queries.delete_database(rpt_db_name)
        sql_queries.delete_database(staging_db_name)
        # create blank reporting and staging DBs
        cr = CommandRunner()
        urv_input_spec = UrvCliInputSpec()
        urv_input_spec.set_parameters(action="CREATE_RPT_DB",
                                      reporting_config_db_server="localhost",
                                      reporting_db_server="localhost",
                                      reporting_db_name=rpt_db_name,
                                      staging_db_name=staging_db_name)

        cr.load_input_spec(urv_input_spec)
        cr.run_command()
        created_databases.append(rpt_db_name)
        created_databases.append(staging_db_name)
    yield _create_rpt_db
    for database in created_databases:
        sql_queries.delete_database(database)


@pytest.fixture
def upsize_and_populate_db():
    def _upsize_and_populate_db(configuration_name,
                                rpt_db_name,
                                staging_db_name,
                                isam_to_sql=False,
                                rpt_db_population=False,
                                ):
        db_config = DatabaseConfiguration(configuration_name)
        db_config.database_parameters.ISAMDB = configuration_name
        db_config.database_parameters.ISAMDBLocation = \
            urv_testdata.get_isam_db_folder(configuration_name)
        db_config.database_parameters.SQLReportingDB = rpt_db_name
        db_config.database_parameters.SQLUpsizedDB = staging_db_name
        db_config.phase_parameters.ISAMToSQL = 'on' if isam_to_sql else 'off'
        db_config.phase_parameters.ReportingDBPopulation = 'on' if rpt_db_population else 'off'
        xml_generator = XmlGenerator()
        xml_generator.add_database_configuration(db_config)
        xml_generator.generate(settings.SOE_ADMIN_DEFAULT_CONFIG_FILE)
        cr = CommandRunner()
        soeadmin_input_spec = SoeAdminInputSpec()
        soeadmin_input_spec.set_parameters(xml_config_file=
                                      settings.SOE_ADMIN_DEFAULT_CONFIG_FILE)
        cr.load_input_spec(soeadmin_input_spec)
        cr.run_command()
    return _upsize_and_populate_db
