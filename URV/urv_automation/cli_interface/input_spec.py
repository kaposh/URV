"""CLI Input specification base class."""
from abc import abstractmethod


class InputSpec:
    """
    Input specification base class. Defines CLI parameters.

    ...

    Attributes
    ----------
    tool_executable:
        Returns a path to external tool executable
    tool_arguments:
        Returns a dictionary of available CommandLineArgument

    Methods
    -------
    set_parameter(name, value):
        Sets a parameter value of CommandLineArgument object
    set_parameters(**kwargs):
        Sets multiple parameter values of CommandLineArgument objects
    get_defined_parameters():
        Parse all existing parameters and returns a list of those which are set
    validate_mandatory_parameters():
        Validate all parameters. Raise an Exception if parameter is mandatory,
        but not set.

    """

    @property
    @abstractmethod
    def tool_executable(self):
        """
        Path to the executable.

        Returns
        -------
        str
            Returns a path to external tool executable

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def tool_arguments(self):
        """
        Arguments of the executable.

        Returns
        -------
        dict
            Returns a dictionary of available CommandLineArguments

        """
        raise NotImplementedError()

    def set_parameter(self, name, value):
        """
        Set a parameter value of CommandLineArgument object.

        Parameters
        ----------
        name : str
            The name of a parameter to be set
        value : str
            A new value to be set

        """
        if name not in self.tool_arguments:
            raise KeyError("Parameter {} is not specified".format(name))
        self.tool_arguments[name].set_value(value)

    def set_parameters(self, **kwargs):
        """
        Set multiple parameter values of CommandLineArgument objects.

        Parameters
        ----------
        **kwargs :
            The keyword arguments to be passed to set_parameter(name, value)

        """
        for key, value in kwargs.items():
            self.set_parameter(key, value)

    def get_defined_parameters(self):
        """
        Parse all existing parameters and returns a list of set parameters.

        Returns
        -------
        list
            Returns a list of existing defined parameters

        """
        parameters_list = []
        for parameter in sorted(self.tool_arguments.values(),
                                key=lambda x: x.order):
            key, value = parameter.get_key_value_pair()
            # key_only : only key will be present ie /ForceRptDbUpdate
            if parameter.key_only:
                if key is not None:
                    parameters_list.append(key)
            # value_only : only value will be present ie <path_to_xml_file>
            elif parameter.value_only:
                if value is not None:
                    parameters_list.append(value)
            # use the key value ie /Action CREATE_RPT_DB
            elif key is not None and value is not None:
                parameters_list.extend((key, value))
        return parameters_list

    def validate_mandatory_parameters(self):
        """
        Validate all parameters.

        Raise an Exception if parameter is mandatory, but not set.

        """
        for parameter in self.tool_arguments.values():
            key, value = parameter.get_key_value_pair()
            if parameter.is_mandatory:
                if key is None and not parameter.value_only:
                    raise KeyError(f"Mandatory parameter key {key} has not"
                                   " been defined")
                if value is None and not parameter.key_only:
                    raise ValueError(f"Mandatory parameter value {value} "
                                     "has not been defined")
