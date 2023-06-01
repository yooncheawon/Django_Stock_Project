import pymysql
pymysql.install_as_MySQLdb()
from pathlib import Path
import sys,os
import json
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent

#add
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRET_DEBUG_FILE = os.path.join(ROOT_DIR, '.config_secret/settings_debug.json')
SECRET_KEY = 'django-insecure-1zn+60rw&j(=)mi#3=1$5av8*(62qq840s^+ay$*6obi455%%k'
DEBUG = True
ALLOWED_HOSTS = []


#앱 정의

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stockInfopage.apps.StockinfopageConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'



DATABASES = {

    'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'ykk_stock',
        'PASSWORD': 'test0000', 
        'HOST': '', 
        'PORT': '3306' #공백으로 둬도 동일
    }
}

# 기본키 필드
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#비밀번호 관련 확인

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


LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

