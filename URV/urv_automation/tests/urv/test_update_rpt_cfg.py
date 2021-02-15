from subprocess import CalledProcessError

from urv_automation.cli_interface import CommandRunner
import pytest
from urv_automation.urv import CliInputSpec


def test_update_rpt_cfg_successful(create_rpt_cfg_db):
    """
    This test is testing if the UPDATE_RPT_CFG command successfully runs

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="UPDATE_RPT_CFG",
                                  reporting_config_db_server="localhost")
    cr.load_input_spec(input_spec=urv_input_spec)
    cr.run_command()


def test_update_rpt_cfg_with_no_config_db():
    """
    This test is testing if the UPDATE_RPT_CFG command fails if no config
    database exists

    """
    cr = CommandRunner()
    urv_input_spec = CliInputSpec()
    urv_input_spec.set_parameters(action="UPDATE_RPT_CFG",
                                  reporting_config_db_server="localhost")
    cr.load_input_spec(input_spec=urv_input_spec)
    with pytest.raises(CalledProcessError):
        cr.run_command()
