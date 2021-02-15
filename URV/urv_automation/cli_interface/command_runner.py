"""Runner for external tools command."""
from urv_automation.cli_interface import InputSpec


class CommandRunner:
    """
    Run a command based on its input specifications.

    ...

    Methods
    -------
    load_input_spec(input_spec):
        Loads an input specification
    run_command(value):
        Sets the value.

    """

    def __init__(self):
        self.input_spec = None

    def load_input_spec(self, input_spec):
        """
        Load the input specification.

        Parameters
        ----------
        input_spec : InputSpec
            The input specification to be set

        """
        if not isinstance(input_spec, InputSpec):
            raise TypeError("Input_spec must be InputSpec type, not {}"
                            .format(input_spec.__class__.__name__))
        self.input_spec = input_spec

    def run_command(self):
        """Run the loaded input specification command."""
        import subprocess
        self.input_spec.validate_mandatory_parameters()
        subprocess.check_call(
            [self.input_spec.tool_executable] +  # noqa W504
            self.input_spec.get_defined_parameters(),
        )
