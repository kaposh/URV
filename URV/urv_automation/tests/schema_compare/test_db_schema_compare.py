import os
import pytest

from urv_automation import settings
from urv_automation.sqlserver.sql_package import SqlPackageReportParser
from urv_automation.sqlserver.sql_package import sql_package_tool
from urv_automation.test_data import urv_testdata

reporting_db_name = 'Test_Reporting'
staging_db_name = 'Test_Staging'

# Add fixtures to this module
pytestmark = pytest.mark.usefixtures("create_rpt_cfg_db",
                                     "create_target_snapshots_dir")


@pytest.mark.skip(reason="The schema of staging dbs are likely to change with "
                         "every release. We must consider their value and how "
                         "to deliver diff to the customers")
def test_compare_staging_to_the_snapshot(configuration_name,
                                         create_rpt_db,
                                         upsize_and_populate_db,
                                         ):
    """
    Run the SQL Package tool on the staging DB and compare it to the previously
    saved DB snapshot. Fail the test if they differ

    Parameters
    ----------
    configuration_name : str
        Name of DB configuration to be run in this test
    create_rpt_db
        Refers to create_rpt_db fixture in conftest.py
    upsize_and_populate_db
        Refers to upsize_and_populate_db fixture in conftest.py
    """
    # Create test databases
    create_rpt_db(reporting_db_name, staging_db_name)
    # Fill staging database
    upsize_and_populate_db(configuration_name,
                           reporting_db_name,
                           staging_db_name,
                           isam_to_sql=True)
    # Extract db to the snapshot
    source = urv_testdata.get_snapshot_path(configuration_name, 'staging',
                                            is_source=True)
    target = urv_testdata.get_snapshot_path(configuration_name, 'staging',
                                            is_source=False)
    sql_package_tool.extract_db(staging_db_name, target)
    output_file_path = os.path.join(settings.COMPARE_LOGS_DIR,
                                    f"out_reporting_{configuration_name}.txt"
                                    )

    sql_package_tool.compare_dacpac_files(
        source_file=source,
        target_file=target,
        target_db_name=staging_db_name,
        output_report_path=output_file_path
    )
    rv = SqlPackageReportParser(path_to_report_file=output_file_path)
    assert len(rv.alerts) == 0, f"Some alerts in db schema exist {rv.alerts}"
    assert len(rv.operations) == 0, f"Some operations in db schema exist " \
                                    f"{rv.operations}"


def test_compare_reporting_to_the_snapshot(configuration_name,
                                           create_rpt_db,
                                           upsize_and_populate_db,
                                           ):
    """
    Run the SQL Package tool on the reporting DB and compare it to the
    previously saved DB snapshot. Fail the test if they differ

    Parameters
    ----------
    configuration_name : str
        Name of DB configuration to be run in this test
    create_rpt_db
        Refers to create_rpt_db fixture in conftest.py
    upsize_and_populate_db
        Refers to upsize_and_populate_db fixture in conftest.py
    tmpdir
        Refers to tmpdir fixture https://docs.pytest.org/en/stable/tmpdir.html
    """
    # Create test databases
    create_rpt_db(reporting_db_name, staging_db_name)
    # Fill staging database
    upsize_and_populate_db(configuration_name,
                           reporting_db_name,
                           staging_db_name,
                           isam_to_sql=True,
                           rpt_db_population=True)
    # Extract db to the snapshot
    source = urv_testdata.get_snapshot_path(configuration_name, 'staging',
                                           is_source=True)
    target = urv_testdata.get_snapshot_path(configuration_name, 'staging',
                                           is_source=False)
    sql_package_tool.extract_db(staging_db_name, target)
    output_file_path = os.path.join(settings.COMPARE_LOGS_DIR,
                                    f"out_reporting_{configuration_name}.txt"
                                    )

    sql_package_tool.compare_dacpac_files(
        source_file=source,
        target_file=target,
        target_db_name=staging_db_name,
        output_report_path=output_file_path
    )
    rv = SqlPackageReportParser(path_to_report_file=output_file_path)
    assert len(rv.alerts) == 0, f"Some alerts in db schema exist {rv.alerts}"
    assert len(rv.operations) == 0, f"Some operations in db schema exist " \
                                    f"{rv.operations}"
