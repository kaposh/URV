"""Definition of project settings such as paths to files."""
import os

from urv_automation.test_data import urv_testdata_registry

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

URV_LOGS_DIR = os.path.join(BASE_DIR, 'logs', 'urv')

COMPARE_LOGS_DIR = os.path.join(BASE_DIR, 'logs', 'compare')

SOE_ADMIN_DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'test_data',
                                             'soe_admin_configs',
                                             'configuration.xml')

URV_ROOT_DIR = urv_testdata_registry.get_urv_install_dir()

SOE_ADMIN_ROOT_DIR = urv_testdata_registry.get_soe_admin_install_dir()
