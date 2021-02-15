"""Generator of Soe Admin XML configuration files."""
from xml.dom import minidom
from xml.etree import ElementTree as ET

from urv_automation.soe_admin.xml_generator import DatabaseConfiguration


class XmlGenerator:
    """
    Generate an XML configuration file from DatabaseConfiguration objects.

    ...

    Methods
    -------
    generate(output_file_path):
        Based on the data in database_configurations generates an XML file
    add_database_configuration(database_configuration):
        Adds a new db configuration into database_configurations array
    _set_sub_elements_from_dictionary(parent_element, dictionary_of_values):
        Adds sub-elements into element tree element from dictionary

    """

    encoding = 'ISO-8859-1'

    def __init__(self):
        self.database_configurations = []

    def generate(self, output_file_path):
        """
        Generate an xml from database_configurations array and save it.

        Parameters
        ----------
        output_file_path : str
            Path to the output xml file

        """
        reporting_views_root = ET.Element('ReportingViewsConfiguration')
        db_list = ET.SubElement(reporting_views_root, 'databaselist')
        for database_configuration in self.database_configurations:
            database = ET.SubElement(db_list, 'database')
            ET.SubElement(database, 'name').text = \
                database_configuration.configuration_name
            # Parameters section
            parameters = ET.SubElement(database, 'parameters')
            self._set_sub_elements_from_dictionary(parameters,
                                                   database_configuration.
                                                   database_parameters.
                                                   get_parameters())
            # Phase section
            phase = ET.SubElement(database, 'phase')
            self._set_sub_elements_from_dictionary(phase,
                                                   database_configuration.
                                                   phase_parameters.
                                                   get_parameters())
        # Make the XML pretty
        xml_str = minidom.parseString(ET.tostring(reporting_views_root)). \
            toprettyxml(indent="   ", encoding=self.encoding)
        with open(output_file_path, "w") as f:
            f.write(xml_str.decode(self.encoding))

    def add_database_configuration(self, database_configuration):
        """
        Add a new db configuration object into database_configurations array.

        Parameters
        ----------
        database_configuration : DatabaseConfiguration
            Database configuration object holding database settings

        """
        if not isinstance(database_configuration, DatabaseConfiguration):
            raise TypeError("Parameter must be type of {}"
                            .format(DatabaseConfiguration.__name__))
        self.database_configurations.append(database_configuration)

    @staticmethod
    def _set_sub_elements_from_dictionary(parent_element, dict_of_values):
        """
        Add a non nonetype sub-elements into ET element from dictionary.

        * If property value is string, set as string
        * If property value is bool, convert to lowercase string

        Parameters
        ----------
        parent_element : SubElement
            Parent element tree object for which sub-elements will be created
        dict_of_values : dict
            Dictionary of sub-element's names ant their values

        """
        for property_name, property_value in dict_of_values.items():
            if property_value is not None:
                if type(property_value) == bool:
                    property_value = str(property_value).lower()
                ET.SubElement(parent_element, property_name).text = \
                    property_value
