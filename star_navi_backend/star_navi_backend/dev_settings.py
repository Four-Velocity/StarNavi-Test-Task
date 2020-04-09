import os
from .utils import get_yaml, hard_get
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = get_yaml('project')

ALLOWED_HOSTS = ['*']

DEBUG = True

SECRET_KEY = hard_get(data, 'django_secret_key')

DATABASES = {
    # 'default': {
    #     'ENGINE': f'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'TestNewLikes',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    #     'USER': 'StarNaviAdmin',
    #     'PASSWORD': '12345',
    #         }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CLEARBIT_KEY = hard_get(data, 'clearbit_key')
EMAILHUNTER_KEY = hard_get(data, 'emailhunter_key')
ADORABLE_AVATAR = hard_get(data, 'adorable_avatar')

CORS_ORIGIN_ALLOW_ALL = True