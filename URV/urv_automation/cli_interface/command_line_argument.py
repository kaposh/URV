"""Argument of external tool's command."""
from dataclasses import dataclass, field


@dataclass
class CommandLineArgument:
    """
    A class to represent a command line argument and its properties.

    ...

    Methods
    -------
    get_value():
        Gets the value of the parameter.
    get_key_value_pair():
        Gets the key-value pair.
    set_value(value):
        Sets the value.

    """

    parameter_key: str = None
    parameter_value: str = None
    key_only: bool = False
    value_only: bool = False
    default_value: str = None
    allowed_values: list = field(default_factory=list)
    is_mandatory: bool = False
    order: int = 99

    def get_value(self):
        """
        Return a command line argument value.

        Returns
        -------
        str
            Returns a parameter_value if set otherwise default_value

        """
        if self.parameter_value is None:
            return self.default_value
        return self.parameter_value

    def get_key_value_pair(self):
        """
        Return a command line argument key-value pair.

        Returns
        -------
        tuple
            Returns a argument key, value pair.

        """
        return self.parameter_key, self.get_value()

    def set_value(self, value):
        """
        Set a new value to parameter_value.

        Parameters
        ----------
        value : str
            The value to be set
        """
        if self.allowed_values and value not in self.allowed_values:
            raise KeyError("Parameter value {} is not defined allowed value {}"
                           .format(value, self.allowed_values))
        else:
            self.parameter_value = value
