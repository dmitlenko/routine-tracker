"""
Development settings template for the project.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "NotSoSecureSecretKey"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa # type: ignore
    }
}


LOGGING['formatters']['colored'] = {  # noqa # type: ignore
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(bold_white)s%(message)s',
}
LOGGING['loggers']['routine_tracker']['level'] = 'DEBUG'  # noqa # type: ignore
LOGGING['handlers']['console']['level'] = 'DEBUG'  # noqa # type: ignore
LOGGING['handlers']['console']['formatter'] = 'colored'  # noqa # type: ignore