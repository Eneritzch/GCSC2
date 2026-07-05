"""
Configuración de Django para el proyecto control_estudiantes.

La configuración lee valores sensibles y dependientes del entorno desde
variables de entorno (o un archivo .env) usando python-decouple, de modo que
el mismo código funcione tanto en desarrollo como en producción (Render).
"""

from pathlib import Path

from decouple import Csv, config

# Directorio raíz del proyecto (donde vive manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Seguridad / entorno
# --------------------------------------------------------------------------
# En desarrollo se usa un valor por defecto; en producción DEBE definirse
# SECRET_KEY como variable de entorno.
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-clave-solo-para-desarrollo-cambiar-en-produccion",
)

DEBUG = config("DEBUG", default=True, cast=bool)

# Lista separada por comas: "midominio.com,www.midominio.com"
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,.onrender.com",
    cast=Csv(),
)

# --------------------------------------------------------------------------
# Aplicaciones
# --------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps del proyecto
    "estudiantes",
    "cursos",
    "reportes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise sirve archivos estáticos en producción sin un servidor extra.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------------------------------
# Base de datos
# --------------------------------------------------------------------------
# Por defecto SQLite (desarrollo). En producción, si se define DATABASE_URL,
# se parsea automáticamente (ej. Postgres de Render).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = config("DATABASE_URL", default="")
if DATABASE_URL:
    import dj_database_url

    DATABASES["default"] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=600, ssl_require=True
    )

# --------------------------------------------------------------------------
# Validación de contraseñas
# --------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

# --------------------------------------------------------------------------
# Internacionalización
# --------------------------------------------------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Archivos estáticos
# --------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Almacenamiento comprimido y con versión gestionado por WhiteNoise.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL a la que redirige el CRUD tras crear/editar/borrar.
LOGIN_URL = "/"
