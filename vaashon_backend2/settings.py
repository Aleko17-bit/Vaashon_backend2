from pathlib import Path
import os

# -----------------------------
# BASE DIR
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# SECURITY
# -----------------------------
SECRET_KEY = 'django-insecure-63t^8yz7f8x$on8oi+ee)krtx8c$q6)+e9i-z0^*kfsxq36832'
DEBUG = True
ALLOWED_HOSTS = ["*"]  # Allow all hosts during development

# -----------------------------
# APPLICATIONS
# -----------------------------
INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
    'payments.apps.PaymentsConfig',
]

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vaashon_backend2.urls'

# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # project-level templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vaashon_backend2.wsgi.application'

# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# -----------------------------
# MEDIA FILES
# -----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# DEFAULT PRIMARY KEY
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------
# MPESA SETTINGS
# -----------------------------
MPESA_ENV = "sandbox"  # change to "production" when going live
MPESA_CONSUMER_KEY = "VwPYm8VVVKm9UEg5KmlSOvNYzSLb7xcaPqGOr1XbGtLg5kQP"
MPESA_CONSUMER_SECRET = "nJkFHLoV7HCDS2TgQRhNWmlpMNNZiQ2sGJbQ8MTMx4Q9Rs5eRLgKyyRT52LXqnaT"
MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2b04e70804b352f64584925fe0c719c5c23e3b41e0c04b7a39bdc57f0f6b5b2d79a1"
MPESA_SHORTCODE = "174379"
MPESA_CALLBACK_URL = "https://765573e089e8.ngrok.io/daraja-callback/"

# -----------------------------
# EMAIL SETTINGS (GMAIL SMTP)
# -----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vaashonshop@gmail.com'  # Your Gmail
EMAIL_HOST_PASSWORD = 'blbecmibgggyehqn'  # Replace with Gmail App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Optional: if using a central static folder
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
