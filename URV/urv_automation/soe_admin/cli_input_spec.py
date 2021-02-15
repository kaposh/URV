"""Specification of Soe Admin CLI."""
import os
from dataclasses import dataclass

from urv_automation.cli_interface import CommandLineArgument, InputSpec
from urv_automation.settings import SOE_ADMIN_ROOT_DIR


@dataclass
class CliInputSpec(InputSpec):
    """Concrete input specification class defining SoeAdmin CLI."""

    def __init__(self):
        self._input_parameters = \
            dict(
                action=CommandLineArgument(
                    parameter_key="AutoSQLUpsize",
                    key_only=True,
                    default_value='True',
                    order=1,
                    is_mandatory=True,
                ),
                xml_config_file=CommandLineArgument(
                    value_only=True,
                    order=2,
                    is_mandatory=True,

                ),
                data_set=CommandLineArgument(
                    value_only=True,
                    order=3,
                ),
            )

    @property
    def tool_arguments(self):
        """Return Soe Admin input parameters."""
        return self._input_parameters

    tool_executable = os.path.join(SOE_ADMIN_ROOT_DIR, 'SoeAdmin.exe')
