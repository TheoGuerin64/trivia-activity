from pydantic import ValidationError
from socketio import AsyncNamespace
from socketio.exceptions import ConnectionRefusedError

from api import APIError, discord

from .db import Session
from .models import Auth
from .schemas import User
from .settings import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET


class Events(AsyncNamespace):
    async def on_connect(
        self, sid: str, environ: dict[str, str], raw_auth: dict[str, str]
    ) -> None:
        try:
            auth = Auth.model_validate(raw_auth)
        except ValidationError as error:
            raise ConnectionRefusedError(error.json())

        try:
            await discord.getToken(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, auth.code)
        except APIError as e:
            raise ConnectionRefusedError(str(e))

        await self.enter_room(sid, auth.channel_id)

        user = User(sid=sid)
        with Session() as session:
            session.add(user)
            session.commit()
