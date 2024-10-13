import os

from django.test import TestCase

from ..utils.misc import get_env, yaml_coerce


class MiscTestCase(TestCase):
    def setUp(self):
        # Set the environment variable
        os.environ["TEST_ENV_VAR"] = "test"

    def test_get_env(self):
        # Test that the function returns the correct value
        self.assertEqual(
            get_env("TEST_ENV_VAR", default="test"),
            "test",
            "get_env should return value of the environment variable",
        )

    def test_yaml_coerce(self):
        # Check if the function coerces the value correctly
        # Test with boolean values
        self.assertTrue(yaml_coerce("true"), "yaml_coerce should coerce 'true' to True")
        self.assertFalse(yaml_coerce("false"), "yaml_coerce should coerce 'false' to False")

        # Test with integer and float values
        self.assertEqual(yaml_coerce("1"), 1, "yaml_coerce should coerce '1' to 1")
        self.assertEqual(yaml_coerce("1.0"), 1.0, "yaml_coerce should coerce '1.0' to 1.0")

        # String values should be returned as is
        self.assertEqual(yaml_coerce("test"), "test", "yaml_coerce should return the value as is")

        # Test with Python objects
        # with list
        self.assertEqual(yaml_coerce("[]"), [], "yaml_coerce should coerce '[]' to []")

        # and with dictionary
        self.assertEqual(
            yaml_coerce("{'a':1}"),
            {'a': 1},
            "yaml_coerce should coerce '{'a':1}' to {'a': 1}",
        )
