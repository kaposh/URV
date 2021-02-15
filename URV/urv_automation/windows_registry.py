"""Functionality related to manipulation with windows registries."""
import winreg


def get_software_32bit_registry_key():
    """Get path to 32bit software registry."""
    software32key = "SOFTWARE\\Wow6432Node"
    if does_registry_subkey_exist(winreg.HKEY_LOCAL_MACHINE, software32key):
        return software32key
    return "SOFTWARE"


def does_registry_subkey_exist(registry, key_path):
    """
    Check if the key path for registry exists.

    Parameters
    ----------
    registry : str
        Registry name ie HKEY_LOCAL_MACHINE
    key_path : str
        Path to key within the registry

    Returns
    -------
    bool
        Returns true if key_path exists, false if does not exist
    """
    try:
        registry = winreg.ConnectRegistry(None, registry)
        winreg.OpenKey(registry, key_path)
        return True
    except FileNotFoundError:
        return False


def get_attributes(registry, key_path):
    """
    Get registry attributes.

    Parameters
    ----------
    registry : str
        Registry name ie HKEY_LOCAL_MACHINE
    key_path : str
        Path to key within the registry

    Returns
    -------
    dict
        Returns dict of attribute keys and values
    """
    key = winreg.OpenKey(registry, key_path, 0, winreg.KEY_READ)
    key_dict = {}
    i = 0
    while True:
        try:
            subvalue = winreg.EnumValue(key, i)
        # WindowsError is raised when i is out of index of key
        except WindowsError:
            break
        key_dict[subvalue[0]] = subvalue[1]
        i += 1
    return key_dict


def get_attribute_value(registry, key_path, name):
    """
    Get registry attribute value.

    Parameters
    ----------
    registry : str
        Registry name ie HKEY_LOCAL_MACHINE
    key_path : str
        Path to key within the registry
    name : str
        Attribute name

    Returns
    -------
    str
        Return a value of selected attribute
    """
    all_attributes = get_attributes(registry, key_path)
    return all_attributes.get(name)


def set_attribute(registry, key_path, name, value):
    """
    Set the attribute of registry on specific path.

    Parameters
    ----------
    registry : str
        Registry name ie HKEY_LOCAL_MACHINE
    key_path : str
        Path to key within the registry
    name : str
        Attribute name
    value : str
        Attribute value
    """
    key = winreg.OpenKey(registry, key_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)


def create_subkey(registry, key_path):
    """
    Set the attribute of registry on specific path.

    Parameters
    ----------
    registry : str
        Registry name ie HKEY_LOCAL_MACHINE
    key_path : str
        Path to key within the registry
    """
    winreg.CreateKey(registry, key_path)
