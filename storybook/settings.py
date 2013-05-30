import os

# Import the proper settings_[environment].py file (defaults to dev)
DJANGO_ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'dev')
exec('from settings_%s import *' % DJANGO_ENVIRONMENT)
