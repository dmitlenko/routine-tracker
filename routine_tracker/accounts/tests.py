from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from .models import UserProfile

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="pass123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="pass123")

    def test_create_user_success(self):
        self.assertEqual(User.objects.count(), 2)

    def test_email_uniqueness(self):
        # Email must be unique across all users
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="user1@example.com", password="pass123")

    def test_string_representation(self):
        self.assertEqual(str(self.user1), "user1@example.com")


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user1@example.com", password="pass123")
        self.profile = UserProfile.objects.create(user=self.user, dark_mode=True)

    def test_create_profile_success(self):
        # Profile should be created with default values
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(self.profile.preferred_language, UserProfile.Language.ENGLISH)
        self.assertEqual(self.profile.time_zone, ("UTC", "UTC"))
        self.assertEqual(self.profile.profile_completeness, 0)

    def test_profile_one_to_one_constraint(self):
        # Creating another profile for the same user should raise an error
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(user=self.user)

    def test_profile_dark_mode_nullability(self):
        # Ensure that setting dark_mode to None doesn't raise issues
        self.profile.dark_mode = None
        self.profile.save()
        self.assertIsNone(self.profile.dark_mode)

    def test_profile_string_representation(self):
        self.assertEqual(str(self.profile), "user1@example.com profile")

    def test_preferred_language_choices(self):
        # Test that invalid language choices raise validation errors
        self.profile.preferred_language = "fr"  # Invalid choice
        with self.assertRaises(ValidationError):
            self.profile.full_clean()  # Validates model fields

    def test_user_deletion_cascades_to_profile(self):
        # Deleting a user should delete the associated profile
        self.user.delete()
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_edge_case_empty_timezone(self):
        # Test setting an empty string as the time zone
        self.profile.time_zone = ""
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_profile_completeness_bounds(self):
        # Ensure profile_completeness is non-negative
        self.profile.profile_completeness = -1
        with self.assertRaises(ValidationError):
            self.profile.full_clean()
