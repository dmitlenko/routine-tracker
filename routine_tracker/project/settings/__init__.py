import os.path

from pathlib import Path
from split_settings.tools import include, optional

from routine_tracker.core.utils.misc import get_env

# Base directory of the project
# This is the directory where the manage.py file is located
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variable prefix for settings
ENV_SETTINGS_PREFIX = 'RT_'

# Define the path to the development settings file
# by default, it is located in the local directory
# can be overridden by setting the LOCAL_SETTINGS_PATH environment variable
LOCAL_SETTINGS_PATH = get_env(f'{ENV_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH', BASE_DIR.parent / 'local/settings.dev.py')

# If the path is not absolute, make it absolute
# to avoid issues with the split-settings library
if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = BASE_DIR / LOCAL_SETTINGS_PATH

# Include the settings files
include(
    'base.py',
    'deployment.py',
    'custom.py',
    optional(str(LOCAL_SETTINGS_PATH)),
    'env.py',
)
