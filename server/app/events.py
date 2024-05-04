from pydantic import ValidationError
from socketio import AsyncNamespace
from sqlalchemy.exc import NoResultFound

from api import APIError, discord

from .db import Session
from .models import Auth
from .schemas import User
from .settings import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET


class Events(AsyncNamespace):
    async def on_connect(self, sid: str, environ: dict[str, str], raw_auth: dict[str, str]) -> bool:
        try:
            auth = Auth.model_validate(raw_auth)
            token = await discord.token(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, auth.code)
            me = await discord.me(token["access_token"])
        except (ValidationError, APIError):
            return False

        async with Session() as session:
            try:
                user = await User.get_by_discord_id(session, me["id"])
            except NoResultFound:
                user = await User.create(
                    session,
                    discord_id=me["id"],
                    socket_id=sid,
                    channel_id=auth.channel_id,
                    connected=True,
                )
            else:
                user.socket_id = sid
                user.connected = True
            await session.commit()

        async with self.session(sid) as sessione:
            sessione["user_id"] = user.id

        return True

    async def on_disconnect(self, sid: str) -> None:
        async with self.session(sid) as session:
            user_id = session["user_id"]

        async with Session() as session:
            user = await session.get(User, user_id)
            assert user is not None
            user.connected = False
            await session.commit()
