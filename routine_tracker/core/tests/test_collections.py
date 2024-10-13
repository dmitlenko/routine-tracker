from django.test import TestCase

from ..utils.collections import deep_update


class CollectionsTestCase(TestCase):
    """
    Test case for the collections module.
    """

    def test_deep_update(self):
        """
        Method to test the deep_update function.
        """

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

        # Define the expected dictionary
        expected_dict = {
            "a": 4,
            "b": {"c": 5, "d": 3},
        }

        # Check that the base dictionary was updated correctly
        self.assertEqual(
            updated_dict,
            expected_dict,
            "deep_update should update the base dictionary correctly",
        )
