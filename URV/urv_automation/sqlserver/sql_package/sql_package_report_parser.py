"""Parser of report generated by SQL package tool."""

from xml.etree import ElementTree as ET


class SqlPackageReportParser:
    """
    Sql package report parser.

    ...

    Attributes
    ----------
    alerts:
        Dictionary of all alert types with corresponding issues
    operations:
        Dictionary of all operation types with corresponding values

    """

    ns = {'default': 'http://schemas.microsoft.com/sqlserver/dac/DeployReport/'
                     '2012/02',
          }

    def __init__(self, path_to_report_file):
        """
        Parse an xml file into the ET object.

        Parameters
        ----------
        path_to_report_file : str
            Path to xml file to be parsed

        """
        tree = ET.parse(path_to_report_file)
        self.xml_root = tree.getroot()

    def _get_element(self, category_name, element_name):
        """
        Get a dictionary of category types with corresponding element names.

        Returns
        -------
        dict
            Dictionary of category names containing array of elements

        """
        existing_element = {}
        for alert in self.xml_root.findall(
                f"default:{category_name}s/default:{category_name}", self.ns):
            existing_element[alert.attrib["Name"]] = []
            for issue in alert.findall(f"default:{element_name}", self.ns):
                existing_element[alert.attrib["Name"]].append(
                    issue.attrib["Value"])
        return existing_element

    @property
    def alerts(self):
        """
        Get a dictionary of all alert types with corresponding issues.

        Returns
        -------
        dict
            Dictionary of alert names and array of issues

        """
        return self._get_element('Alert', 'Issue')

    @property
    def operations(self):
        """
        Get a dictionary of all operation types with corresponding issues.

        Returns
        -------
        dict
            Dictionary of operation names and array of values

        """
        return self._get_element('Operation', 'Item')