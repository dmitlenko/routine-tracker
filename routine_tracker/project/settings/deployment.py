"""
Deployment settings for the project.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = NotImplemented

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = []

# Static files (CSS, JavaScript, Images)
# will be server from this directory using NGINX
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa # type: ignore
