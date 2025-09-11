"""
Django settings for printing_site project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "change_me_local_dev"
DEBUG = True  # Enable debug mode for development
ALLOWED_HOSTS = ["*"]   # за локална работа и първи деплой

# Check if we're in production (when deployed with domain)
IS_PRODUCTION = os.environ.get('DOMAIN') or not DEBUG

# CSRF and Security Settings for Production
CSRF_TRUSTED_ORIGINS = [
    "https://3d-printing.beekeeperassistant.com",
    "http://3d-printing.beekeeperassistant.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Additional security settings for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Let nginx handle SSL redirect

# CSRF settings
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_AGE = 31449600  # 1 year
CSRF_USE_SESSIONS = False

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'prints',  # Our 3D printing app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Additional settings for reverse proxy
if IS_PRODUCTION:
    # Trust the X-Forwarded-For header from nginx
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

ROOT_URLCONF = 'printing_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'printing_site.wsgi.application'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# По подразбиране локално ползваме SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Ако в средата има DATABASE_URL (ще зададем в Portainer), се ползва MySQL
DB_URL = os.environ.get("DATABASE_URL")
if DB_URL:  # формат: mysql://user:pass@mysql:3306/appdb?charset=utf8mb4
    from urllib.parse import urlparse, parse_qs
    u = urlparse(DB_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": u.path.lstrip("/"),
            "USER": u.username,
            "PASSWORD": u.password,
            "HOST": u.hostname,
            "PORT": u.port or "3306",
            "OPTIONS": {"charset": parse_qs(u.query).get("charset", ["utf8mb4"])[0]},
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Additional static files directories for development
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Additional production settings
USE_TZ = True

# Session and security settings
if IS_PRODUCTION:
    # Production security settings
    SESSION_COOKIE_SECURE = True  # Only send session cookies over HTTPS
    CSRF_COOKIE_SECURE = True     # Only send CSRF cookies over HTTPS
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Development settings
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Common security settings
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# For production deployment, you should set these environment variables:
# SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
# DOMAIN = os.environ.get('DOMAIN', '')  # Set this to your domain in production
