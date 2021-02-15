"""Specification of URV CLI."""
import os
import tempfile

from urv_automation import settings
from urv_automation.cli_interface import CommandLineArgument, InputSpec


def get_run_location_dir():
    """Get temporary folder to be set as run location."""
    temp_path = os.path.join(tempfile.gettempdir(), 'urv')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    return temp_path


class CliInputSpec(InputSpec):
    """
    Concrete input specification class defining URV CLI.

    Attributes
    ----------
    tool_arguments:
        Returns a dictionary of available arguments
    tool_executable:
        Path to URV tool executable
    """

    def __init__(self):
        self._input_parameters = \
            dict(
                action=CommandLineArgument(
                    parameter_key="/Action",
                    allowed_values=["CREATE_RPT_CFG",
                                    "UPDATE_RPT_CFG",
                                    "CREATE_RPT_DB",
                                    "UPGRADE_ALL_RPT_DBS",
                                    "REMOVE_RPT_DB",
                                    "REMOVE_ALL_RPT_DBS",
                                    "UPGRADE_RPT_DB",
                                    "REMOVE_RPT_CFG",
                                    "ADD_RPT_DB"],
                    is_mandatory=True,
                ),
                reporting_config_db_server=CommandLineArgument(
                    parameter_key="/ReportingConfigDbServer",
                    is_mandatory=True,
                ),

                #  Run location parameter must be specified, otherwise URV will
                #  try to copy its own executable to the default run location
                #  dir - which is its own directory
                run_location_dir=CommandLineArgument(
                    parameter_key="/RunLocationDir",
                    default_value=get_run_location_dir(),
                ),
                reporting_db_server=CommandLineArgument(
                    parameter_key="/ReportingDbServer",
                ),
                reporting_db_name=CommandLineArgument(
                    parameter_key="/ReportingDbName",
                ),
                reporting_dbdata_dir=CommandLineArgument(
                    parameter_key="/ReportingDbdataDir",
                ),
                reporting_dblog_dir=CommandLineArgument(
                    parameter_key="/ReportingDblogDir",
                ),
                staging_db_name=CommandLineArgument(
                    parameter_key="/StagingDbName",
                ),
                staging_dbdata_dir=CommandLineArgument(
                    parameter_key="/StagingDbDataDir",
                ),
                staging_dblog_dir=CommandLineArgument(
                    parameter_key="/StagingDbLogDir",
                ),
                source_db_server=CommandLineArgument(
                    parameter_key="/SourceDbserver",
                ),
                extract_use_ssis=CommandLineArgument(
                    parameter_key="/ExtractUseSSIS",
                ),
                ssis_run_attempts=CommandLineArgument(
                    parameter_key="/SSISRunAttempts",
                ),
                ssrs_report_server_url=CommandLineArgument(
                    parameter_key="/SSRSReportServerURL",
                ),
                ssrs_reports_folder=CommandLineArgument(
                    parameter_key="/SSRSReportsFolder",
                ),
                ssrs_data_source_name=CommandLineArgument(
                    parameter_key="/SSRSDataSourceName",
                ),
                ssrs_full_model_name=CommandLineArgument(
                    parameter_key="/SSRSFullModelName",
                ),
                ssrs_no_upload=CommandLineArgument(
                    key_only=True,
                ),
                force_rpt_db_update=CommandLineArgument(
                    key_only=True,
                ),
                refresh_custom_screens=CommandLineArgument(
                    "/RefreshCustomScreens",
                ),
                log_file=CommandLineArgument(
                    parameter_key="/Logfile",
                    default_value=os.path.join(settings.URV_LOGS_DIR,
                                               "workflow_log.txt"),
                ),
            )

    tool_executable = os.path.join(settings.URV_ROOT_DIR,
                                   'ReportingViewsDeployDb.exe')

    @property
    def tool_arguments(self):
        """Return URV input parameters."""
        return self._input_parameters
