from typing import Dict


def deep_update(base_dict: Dict, update_with: Dict) -> Dict:
    """
    Recursively update the base dictionary with the update_with dictionary.
    """

    # Iterate over the items in the update_with dictionary
    for key, value in update_with.items():
        # If the value is a dictionary, recursively update the base dictionary
        if isinstance(value, dict):
            # If the key is not in the base dictionary, add it
            base_dict[key] = deep_update(base_dict.get(key, {}), value)
        else:
            # Otherwise, update the value in the base dictionary
            base_dict[key] = value

    # Return the updated base dictionary
    return base_dict
