import socketio
from aiohttp import web
from pydantic import ValidationError
from socketio.exceptions import ConnectionRefusedError

from api import APIError, discord
from models import Auth
from settings import DISCORD_CLIENT_ID

sio = socketio.AsyncServer(
    async_mode="aiohttp",
    cors_allowed_origins=f"https://{DISCORD_CLIENT_ID}.discordsays.com",
)
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid: str, environ: dict[str, str], raw_auth: dict[str, str]) -> None:
    try:
        auth = Auth.model_validate(raw_auth)
    except ValidationError as error:
        raise ConnectionRefusedError(error.json())

    try:
        await discord.getToken(auth.code)
    except APIError as e:
        raise ConnectionRefusedError(str(e))


if __name__ == "__main__":
    web.run_app(app, port=3000)
