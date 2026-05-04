import os

from django.core.wsgi import get_wsgi_application
#default settings file 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
#WSGI application for normal http requests
application = get_wsgi_application()
