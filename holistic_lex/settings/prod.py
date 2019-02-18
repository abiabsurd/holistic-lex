from holistic_lex.settings.base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Configure Django App for Heroku.
django_heroku.settings(locals())
