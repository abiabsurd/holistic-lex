from holistic_lex.settings.base import *

DEBUG = True
SECRET_KEY = 'CHANGE_THIS'

# Configure Django App for Heroku.
django_heroku.settings(locals())
