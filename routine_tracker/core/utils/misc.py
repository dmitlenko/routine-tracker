import os
from typing import Any, Union

import yaml


def yaml_coerce(value: Union[str, Any]) -> Any:
    """
    Coerce a value to a Python object using PyYAML. This function is useful for
    converting environment variables to Python objects.
    """

    # Convert value to a Python object
    if isinstance(value, str):
        return yaml.safe_load(f"dummy: {value}")["dummy"]

    # If the value is not a string, return it as is
    return value


def get_env(name: str, default: Any = None) -> Any:
    """
    Get an environment variable with the given name. If the environment variable
    is not set, return the default value.
    """

    return yaml_coerce(default) if (value := os.environ.get(name)) is None else yaml_coerce(value)
