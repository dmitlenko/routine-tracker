from routine_tracker.core.utils.collections import deep_update
from routine_tracker.core.utils.settings import get_env_settings

# Update the global settings with the environment variables
# that start with the prefix 'RT_'.
deep_update(globals(), get_env_settings(ENV_SETTINGS_PREFIX))  # noqa # type: ignore
