import socketio
from pydantic import ValidationError
from socketio.exceptions import ConnectionRefusedError

from api import APIError, discord
from models import Auth
from settings import DISCORD_CLIENT_ID

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=f"https://{DISCORD_CLIENT_ID}.discordsays.com",
)
app = socketio.ASGIApp(sio)


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

    await sio.enter_room(sid, auth.channel_id)


if __name__ == "__main__":
    import uvicorn

    from settings import DEV

    uvicorn.run(
        "__main__:app", ws_max_size=2**12, host="0.0.0.0", port=3000, reload=DEV
    )
