"""Getting the atteibutes of installed SOE software."""
import os

from urv_automation import windows_registry

import winreg


def get_testdata_install_dir():
    """Get the testdata install directory from registry."""
    return get_soe_product_attribute_value("urv-testdata", "Path")


def get_soe_admin_install_dir():
    """Get the Soe Admin install directory from registry."""
    return get_soe_product_attribute_value("SOE Admin", "InstallRoot")


def get_urv_install_dir():
    """Get the URV install directory from registry."""
    return get_soe_product_attribute_value("EXACT Reporting Views",
                                           "RunLocationDir")


def get_soe_product_attribute_value(product_name, attribute_name):
    """Get the attribute of the product located in SOE software registry."""
    software_key = windows_registry.get_software_32bit_registry_key()
    registry_path = os.path.join(software_key, "Software of Excellence",
                                 product_name)
    if not windows_registry.does_registry_subkey_exist(
            winreg.HKEY_LOCAL_MACHINE, registry_path):
        raise FileNotFoundError(f"Product key was found {registry_path}")
    return windows_registry.get_attribute_value(winreg.HKEY_LOCAL_MACHINE,
                                                registry_path,
                                                attribute_name)
