import socketio
from aiohttp import web
from socketio.exceptions import ConnectionRefusedError

from api import APIError, discord

sio = socketio.AsyncServer(cors_allowed_origins="*")
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


@sio.event
def disconnect(sid: str):
    print("disconnect ", sid)


if __name__ == "__main__":
    web.run_app(app, port=3000)
