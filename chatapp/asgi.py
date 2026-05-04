import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

django_asgi_app = get_asgi_application()

from rtchat import routing 


#ASGI routes for http requests and web socket connection
application = ProtocolTypeRouter({
    "http" : django_asgi_app,
    
    #Websocket requests are authenticated and then are matched to chat routes
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        
    ),
})