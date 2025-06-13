import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Important: configure Django BEFORE importing anything that uses models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WageWay.settings')
django.setup()

import notifications.routing  # must be AFTER setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(notifications.routing.websocket_urlpatterns)
    ),
})
