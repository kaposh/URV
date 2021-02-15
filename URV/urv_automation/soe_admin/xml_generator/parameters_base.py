"""Base class for parameters dataclass of XML configuration for Soe Admin."""
from dataclasses import dataclass
from dataclasses import fields


@dataclass
class ParametersBase:
    """
    Base class for parameters dataclass.

    ...

    Methods
    -------
    get_parameters():
        Gets the dictionary of attributes with their values
    set_parameter(name, value)):
        Sets a parameter value of dataclass attribute
    set_parameters(**kwargs):
        Sets multiple parameter values of dataclass attributes

    """

    def get_parameters(self):
        """
        Get the dictionary of attributes with their values.

        Returns
        -------
        dict
            Returns a dictionary of attribute names and their values

        """
        return {field.name: getattr(self, field.name)
                for field in fields(self)}

    def set_parameter(self, name, value):
        """
        Set a parameter value of dataclass attribute.

        Parameters
        ----------
        name : str
            The name of a attribute to be set
        value : str
            A new value to be set

        """
        setattr(self, name, value)

    def set_parameters(self, **kwargs):
        """
        Set multiple parameter values of dataclass attributes.

        Parameters
        ----------
        **kwargs :
            The keyword arguments to be passed to set_parameter(name, value)

        """
        for key, value in kwargs.items():
            self.set_parameter(key, value)
