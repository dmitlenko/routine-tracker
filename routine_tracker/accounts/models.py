from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with email as the unique identifier
    """

    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    User profile model with additional user preferences
    """

    class Language(models.TextChoices):
        """
        Language choices for the user profile
        """

        ENGLISH = 'en', 'English'
        UKRAINIAN = 'uk', 'Ukrainian'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dark_mode = models.BooleanField(default=None, null=True)
    preferred_language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.ENGLISH,
    )
    time_zone = models.CharField(max_length=100, default='UTC')
    profile_completeness = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"
