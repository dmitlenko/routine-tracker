from typing import Dict, NamedTuple


def dep_dict(name_tuple: NamedTuple) -> Dict:
    """Converts a NamedTuple to a dictionary

    Args:
        name_tuple (NamedTuple): NamedTuple to convert

    Returns:
        Dict: Dictionary representation of the NamedTuple
    """
    return {field: getattr(name_tuple, field) for field in name_tuple._fields}
