from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import py_compiler.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(py_compiler.routing.websocket_urlpatterns))
})