import pytz
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model with email as the unique identifier
    """

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    User profile model with additional user preferences
    """

    class Language(models.TextChoices):
        """
        Language choices for the user profile
        """

        ENGLISH = 'en', _('English')
        UKRAINIAN = 'uk', _('Ukrainian')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dark_mode = models.BooleanField(default=None, null=True, verbose_name=_('Dark mode'))
    preferred_language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.ENGLISH,
        verbose_name=_('Preferred language'),
    )
    time_zone = models.CharField(
        max_length=100,
        verbose_name=_('Time zone'),
        default=('UTC', 'UTC'),
        choices=[(tz, tz) for tz in pytz.all_timezones],
    )
    profile_completeness = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return _("{username} profile").format(username=self.user.email)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')
