from .settings import *  # NOQA

TEST = True
DEBUG = False

# Always use OTPAdminConfig in tests to keep env same as prod (OTPAdminConfiig has different permission checks)
if "django.contrib.admin" in INSTALLED_APPS:
    INSTALLED_APPS.remove("django.contrib.admin")
if "bonfire.apps.OTPAdminConfig" not in INSTALLED_APPS:
    INSTALLED_APPS.append("bonfire.apps.OTPAdminConfig")


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

DEFAULT_FILE_STORAGE = "django.core.files.storage.InMemoryStorage"
STATICFILES_STORAGE = "django.core.files.storage.InMemoryStorage"

CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = "memory://"
CELERY_BACKEND = "memory"

SILENCED_SYSTEM_CHECKS = [
    "debug_toolbar.W001",  # Debug toolbar excluded in tests
]
