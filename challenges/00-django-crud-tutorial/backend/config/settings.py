"""
Django settings for the Campus Club Desk tutorial project.

READ THIS FILE FIRST when debugging.
A request only reaches your views if the pieces below agree:

  manage.py
    → DJANGO_SETTINGS_MODULE = "config.settings"   (this module)
    → ROOT_URLCONF = "config.urls"                 (URL router)
    → INSTALLED_APPS includes "clubs" and "events" (models / apps load)
    → DATABASES points at sqlite                    (ORM persistence)

If an app is missing from INSTALLED_APPS, its models/migrations will break.
If ROOT_URLCONF is wrong, every URL 404s.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-only-django-crud-tutorial-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- Apps -----------------------------------------------------------------
# Django discovers models, management commands, and app config from here.
# This project has TWO local apps: clubs + events.
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "clubs",    # App 1 — club CRUD  → clubs/urls.py
    "events",   # App 2 — event CRUD → events/urls.py
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# --- URL root -------------------------------------------------------------
# Django loads this module and uses its `urlpatterns` to match every request.
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Database -------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}
