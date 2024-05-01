import socketio
from aiohttp import web
from socketio.exceptions import ConnectionRefusedError

from api import APIError, discord
from settings import DISCORD_CLIENT_ID

sio = socketio.AsyncServer(
    async_mode="aiohttp",
    cors_allowed_origins=f"https://{DISCORD_CLIENT_ID}.discordsays.com",
)
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid: str, environ: dict, auth: dict) -> bool | None:
    if not auth:
        return False
    code = auth.get("code")
    if not code:
        return False

    try:
        await discord.getToken(code)
    except APIError as e:
        raise ConnectionRefusedError(str(e))


if __name__ == "__main__":
    web.run_app(app, port=3000)
