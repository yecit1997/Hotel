"""
Django settings for gestionHotel project.
"""

from datetime import timedelta
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad y Configuración de Entorno ---
# Siempre cargar variables de entorno ANTES de usarlas
# SECRET_KEY (requerido)
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable de entorno SECRET_KEY no está configurada.")

# DEBUG (convertir a booleano de forma segura)
DEBUG = (os.getenv('DEBUG', 'False').lower() == 'true')

# ALLOWED_HOSTS (manejar múltiples hosts)
ALLOWED_HOSTS_STR = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR if host.strip()]
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # Para desarrollo si no se especifica

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    "rest_framework_simplejwt.token_blacklist", # Necesario si ROTATE_REFRESH_TOKENS es True
]

LOCAL_APPS = [
    'usuario.apps.UsuarioConfig',
    'habitacion.apps.HabitacionConfig',
    'cliente.apps.ClienteConfig',
    'reserva.apps.ReservaConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestionHotel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Añadir para usar debug en templates
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestionHotel.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Configuración para SQLite (desarrollo por defecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Opcional: Configuración para MySQL (ejemplo con variables de entorno) ---
# DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3') # Por defecto sqlite3
# if DB_ENGINE == 'mysql':
#     DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DB_NAME', 'api_django'),
#         'USER': os.getenv('DB_USER', 'root'),
#         'PASSWORD': os.getenv('DB_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', '127.0.0.1'),
#         'PORT': os.getenv('DB_PORT', '3306'),
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             'charset': 'utf8mb4',
#         },
#     }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-co' # Colombia
TIME_ZONE = 'America/Bogota' # O 'America/Bogota' para Colombia
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Para producción, recolectar estáticos aquí

# Media files (Archivos subidos por los usuarios, como las imágenes de documentos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Modelo de usuario personalizado
AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL', 'usuario.Usuario') # Añadir un default para desarrollo


# Configuracion para la conexion del Frontend
CORS_ALLOWED_ORIGINS_STR = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_STR if origin.strip()]

# O en desarrollo, si lo deseas (pero cuidado en producción):
# CORS_ALLOW_ALL_ORIGINS = DEBUG # Solo en debug, permite todo

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ( # ¡Importante! Añadir permisos por defecto
        'rest_framework.permissions.IsAuthenticated', # Requiere autenticación por defecto
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', # Paginación por defecto
    'PAGE_SIZE': 10, # Número de elementos por página
    'DEFAULT_FILTER_BACKENDS': (
        # 'rest_framework.filters.SearchFilter',
        # 'django_filters.rest_framework.DjangoFilterBackend', # Si usas django-filter
    ),
    # Añadir DEFAULT_RENDERER_CLASSES para consistencia
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # Útil para la API web de desarrollo
    ),
}


#---------------------------------------------------------
'''Implementacion y configuracion de TOKEN con JWT'''
#---------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True, # Cambiado a True para mayor seguridad
    "BLACKLIST_AFTER_ROTATION": True, # Cambiado a True para mayor seguridad
    "UPDATE_LAST_LOGIN": True, # Bueno para saber cuándo fue la última actividad del usuario

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY, # No uses settings.SECRET_KEY aquí, ya lo tienes en el ámbito global
    "VERIFYING_KEY": "", # OK para HS256

    "AUDIENCE": None, # Puedes definir una audiencia si usas múltiples servicios
    "ISSUER": None, # Puedes definir un emisor si usas múltiples servicios
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    # ¡Importante! Aquí debes apuntar a tu serializador personalizado si lo tienes.
    # Por ejemplo, si está en tu app 'usuario' en 'serializers.py'
    "TOKEN_OBTAIN_SERIALIZER": "usuario.serializers.MyTokenObtainPairSerializer", 
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}