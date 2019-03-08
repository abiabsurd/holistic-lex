import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from holistic_lex.settings.base import *


DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
SECRET_KEY = os.environ.get('SECRET_KEY')

sentry_sdk.init(
    dsn='https://cec38e4b1bde476382d69d157fe709b5@sentry.io/1410719',
    integrations=[DjangoIntegration()]
)

# Configure Django App for Heroku.
django_heroku.settings(locals())
