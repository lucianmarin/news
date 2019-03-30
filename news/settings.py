"""
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4^suh^yp2@jm!a!8snts8wb(y2kx4v482km5mnc^+topkpc*!p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'app'
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'jinja2')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'app.jinja.environment',
        }
    }
]

WSGI_APPLICATION = 'news.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newscafe',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '6432'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False
USE_ETAGS = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

FEEDS = [
    "http://rss.sciam.com/scientificamerican-global",
    "http://feeds.reuters.com/news/artsculture",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.reuters.com/reuters/entertainment",
    "http://feeds.reuters.com/reuters/environment",
    "http://feeds.reuters.com/reuters/healthNews",
    "http://feeds.reuters.com/reuters/oddlyEnoughNews",
    "http://feeds.reuters.com/reuters/scienceNews",
    "http://feeds.reuters.com/reuters/technologyNews",
    "http://feeds.macrumors.com/macrumors-front",
    "http://feeds.crackberry.com/crackberry/qbtb",
    "http://feeds.imore.com/theiphoneblog",
    "http://feeds.androidcentral.com/androidcentral",
    "http://feeds.windowscentral.com/wmexperts",
    "http://feeds.feedburner.com/businessinsider",
    "http://feeds.feedburner.com/neowin-main",
    "http://feeds.feedburner.com/petapixel",
    "http://feeds.feedburner.com/thehackersnews",
    "http://feeds.feedburner.com/venturebeat/szyf",
    "http://feeds.feedburner.com/sub/9to5google",
    "http://feeds.feedburner.com/sub/9to5mac",
    "http://feeds.feedburner.com/sub/aeon",
    "http://feeds.feedburner.com/sub/anandtech",
    "http://feeds.feedburner.com/sub/atlantic",
    "http://feeds.feedburner.com/sub/axios",
    "http://feeds.feedburner.com/sub/eff",
    "http://feeds.feedburner.com/sub/electrek",
    "http://feeds.feedburner.com/sub/engadget",
    "http://feeds.feedburner.com/sub/fastcompany",
    "http://feeds.feedburner.com/sub/fubiz",
    "http://feeds.feedburner.com/sub/gsmarena",
    "http://feeds.feedburner.com/sub/longreads",
    "http://feeds.feedburner.com/sub/mspoweruser",
    "http://feeds.feedburner.com/sub/nautilus",
    "http://feeds.feedburner.com/sub/npr",
    "http://feeds.feedburner.com/sub/nytimes/science",
    "http://feeds.feedburner.com/sub/nytimes/tech",
    "http://feeds.feedburner.com/sub/omgubuntu",
    "http://feeds.feedburner.com/sub/polygon",
    "http://feeds.feedburner.com/sub/producthunt",
    "http://feeds.feedburner.com/sub/qz",
    "http://feeds.feedburner.com/sub/register",
    "http://feeds.feedburner.com/sub/semiaccurate",
    "http://feeds.feedburner.com/sub/seth",
    "http://feeds.feedburner.com/sub/smashing",
    "http://feeds.feedburner.com/sub/techcrunch",
    "http://feeds.feedburner.com/sub/verge",
    "http://feeds.feedburner.com/sub/vox",
    "http://feeds.feedburner.com/sub/wired"
]

LINKS = [
    "https://daringfireball.net/feeds/main",
    "https://news.ycombinator.com/rss",
    "https://lobste.rs/rss",
    "http://monocle.io/feed",
    "https://www.designernews.co/?format=rss",
    "https://www.techmeme.com/feed.xml",
    "http://rss.slashdot.org/Slashdot/slashdotMain"
]

TOKEN = "531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0"

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

# Local settings
from news.local import *
