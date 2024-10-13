import os

from django.test import TestCase

from ..utils.settings import get_env_settings


class SettingsTestCase(TestCase):
    """
    Test case for the settings module.
    """

    def setUp(self):
        # Define prefix
        self.prefix = "TEST_ENV_SETTINGS_"
        # Set the environment variables
        os.environ[f"{self.prefix}VAR1"] = "test1"
        os.environ[f"{self.prefix}VAR2"] = "test2"

    def test_get_env_settings(self):
        """
        Method to test the get_env_settings function.
        """

        # Test that the function returns the correct settings
        self.assertEqual(
            get_env_settings(self.prefix),
            {
                "VAR1": "test1",
                "VAR2": "test2",
            },
            "get_env_settings should return the correct settings",
        )
