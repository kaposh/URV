"""Wrapper arounf the CLI of package tool executable."""
import os
import subprocess
from xml.dom import minidom


def get_sql_package_path():
    """
    Return a path to a sql package tool executable.

    Raises an exception if the env variable SQL_PACKAGE_TOOL_DIR does not
    exist

    Returns
    -------
    str
        Path to SQL Package executable

    """
    sql_package_dir = os.environ['SQL_PACKAGE_TOOL_DIR']
    return os.path.join(sql_package_dir, 'sqlpackage.exe')


def extract_db(source_db_name, target_file):
    """
    Call a SQL Package CLI and extracts the existing SQL db into dacpac.

    Parameters
    ----------
    source_db_name : str
        Name of existing SQL database
    target_file : str
        Name of output dacpac file

    """
    command = [get_sql_package_path(),
               '/Action:Extract',
               f'/TargetFile:{target_file}',
               '/SourceServerName:localhost',
               f'/SourceDatabaseName:{source_db_name}']
    subprocess.run(command, check=True)


def compare_dacpac_files(source_file, target_file, target_db_name,
                         output_report_path):
    """
    Compare two existing dacpac files and export the difference to report.

    Parameters
    ----------
    source_file : str
        Source dacpac file for comparision
    target_file : str
        Target dacpac file for comparision
    target_db_name : str
        Target database name
    output_report_path : str
        Path to the output report, where diffs are exported

    """
    command = [get_sql_package_path(),
               '/Action:DeployReport',
               '/TargetFile:{}'.format(target_file),
               '/SourceFile:{}'.format(source_file),
               '/TargetDatabaseName:{}'.format(target_db_name),
               '/SourceTrustServerCertificate:True',
               '/OutputPath:{}'.format(output_report_path)]
    subprocess.run(command, check=True)
    # Make the XML file pretty
    with open(output_report_path, encoding='utf-8') as file:
        data = file.read()
    pretty_content = minidom.parseString(data).toprettyxml(indent="   ")
    with open(output_report_path, 'w') as file:
        file.write(pretty_content)
