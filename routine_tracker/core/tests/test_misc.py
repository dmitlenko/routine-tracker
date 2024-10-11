import os

from ..utils.misc import get_env, yaml_coerce


def test_get_env():
    # Set the environment variable
    os.environ["TEST_ENV_VAR"] = "test"

    # Test that the function returns the correct value
    assert get_env("TEST_ENV_VAR", default="test") == "test", "get_env should return value of the environment variable"


def test_yaml_coerce():
    # Check if the function coerces the value correctly
    assert yaml_coerce("true") is True, "yaml_coerce should coerce 'true' to True"
    assert yaml_coerce("false") is False, "yaml_coerce should coerce 'false' to False"
    assert yaml_coerce("1") == 1, "yaml_coerce should coerce '1' to 1"
    assert yaml_coerce("1.0") == 1.0, "yaml_coerce should coerce '1.0' to 1.0"
    assert yaml_coerce("test") == "test", "yaml_coerce should return the value as is"
    assert yaml_coerce("[]") == [], "yaml_coerce should coerce '[]' to []"
    assert yaml_coerce("{'a':1}") == {'a': 1}, "yaml_coerce should coerce '{'a':1}' to {'a': 1}"
