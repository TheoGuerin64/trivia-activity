import socketio

from .db import init_tables
from .events import Events
from .settings import DISCORD_CLIENT_ID

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=f"https://{DISCORD_CLIENT_ID}.discordsays.com",
)
app = socketio.ASGIApp(sio, on_startup=init_tables)
sio.register_namespace(Events("/"))
