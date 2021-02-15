"""Functionality related to installed testdata for URV."""
import os

from urv_automation.test_data import urv_testdata_registry


def get_urv_testdata_dir():
    """Get path to URV test data folder."""
    return urv_testdata_registry.get_testdata_install_dir()


def get_datasets_dir():
    """Get path to URV test data data sets folder."""
    return os.path.join(get_urv_testdata_dir(), 'datasets')


def get_sql_snapshots_source_dir():
    """Get path to URV test data sql_snapshots_source folder."""
    return os.path.join(get_urv_testdata_dir(), 'sql_snapshots_source')


def get_sql_snapshots_target_dir():
    """Get path to URV test data sql_snapshots_target folder."""
    return os.path.join(get_urv_testdata_dir(), 'sql_snapshots_target')


def get_available_dbs_info():
    """Get the list of databases and their paths."""
    return {db: os.path.join(get_datasets_dir(), db)
            for db in next(os.walk(get_datasets_dir()))[1]}


def get_isam_db_folder(configuration_name):
    """
    Get the dictionary to ISAM database.

    Parameters
    ----------
    configuration_name : str
        Name of DB configuration to be used

    """
    return os.path.join(get_datasets_dir(), configuration_name)


def get_sql_snapshot_filename(configuration_name, snapshot_type):
    """
    Get the name of snapshot for selected configuration and type.

    Parameters
    ----------
    configuration_name : str
        Name of DB configuration
    snapshot_type : str
        Type of snapshot : reporting/staging

    """
    if snapshot_type != 'reporting' or 'staging':
        ValueError("Allowed snapshot types are staging or reporting")
    return f"{configuration_name}_{snapshot_type}.dacpac"


def get_snapshot_path(configuration_name, snapshot_type, is_source=True):
    """
    Get path to th snapshot by configuration name and snapshot type.

    Parameters
    ----------
    configuration_name : str
        Name of DB configuration
    snapshot_type : str
        Type of snapshot : reporting/staging
    is_source : bool
        Is the snapshot source(previous version) or target(current version)

    """
    # Get the folder name
    folder = get_sql_snapshots_target_dir()
    if is_source:
        folder = get_sql_snapshots_source_dir()
    # Get the snapshot name
    file_name = get_sql_snapshot_filename(configuration_name, snapshot_type)
    return os.path.join(folder, file_name)
