# mysite/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

# ?P<room_name>[^/]+)/$
from webViz import consumers

websocket_urlpatterns = [
    url(r'^RTEndpoint/$', consumers.ChatConsumer),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})
