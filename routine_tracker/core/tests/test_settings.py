import os

from ..utils.settings import get_env_settings


def test_get_env_settings():
    # Define prefix
    prefix = "TEST_ENV_SETTINGS_"
    # Set the environment variables
    os.environ[f"{prefix}VAR1"] = "test1"
    os.environ[f"{prefix}VAR2"] = "test2"

    # Test that the function returns the correct settings
    assert get_env_settings(prefix) == {
        "VAR1": "test1",
        "VAR2": "test2",
    }, "get_env_settings should return the correct settings"
