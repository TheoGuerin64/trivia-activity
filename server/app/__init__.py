import socketio

from .db import init_db
from .events import Events
from .settings import DISCORD_CLIENT_ID

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=f"https://{DISCORD_CLIENT_ID}.discordsays.com",
)
app = socketio.ASGIApp(sio, on_startup=init_db)
sio.register_namespace(Events("/"))
