from ..utils.collections import deep_update


def test_deep_update():
    # Define the base dictionary
    base_dict = {
        "a": 1,
        "b": {"c": 2, "d": 3},
    }

    # Define the update_with dictionary
    update_with = {
        "a": 4,
        "b": {"c": 5},
    }

    # Update the base dictionary with the update_with dictionary
    updated_dict = deep_update(base_dict, update_with)

    # Check that the base dictionary was updated correctly
    assert updated_dict == {
        "a": 4,
        "b": {"c": 5, "d": 3},
    }, "deep_update should update the base dictionary correctly"
