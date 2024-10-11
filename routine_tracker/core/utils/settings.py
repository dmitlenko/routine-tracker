import os
from typing import Dict

from .misc import yaml_coerce


def get_env_settings(prefix: str) -> Dict:
    """
    Get all environment variables with the given prefix and return them as a dictionary.
    """

    prefix_len = len(prefix)

    return {key[prefix_len:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)}
