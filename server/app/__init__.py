import socketio

from .events import Events
from .settings import DISCORD_CLIENT_ID

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=f"https://{DISCORD_CLIENT_ID}.discordsays.com",
)
app = socketio.ASGIApp(sio)
sio.register_namespace(Events("/"))
