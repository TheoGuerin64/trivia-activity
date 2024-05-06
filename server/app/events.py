from pydantic import ValidationError
from socketio import AsyncNamespace
from sqlalchemy.exc import NoResultFound

from .api import APIError, discord
from .db import Session
from .db.schemas import Room, User
from .models import Auth
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
                    connected=True,
                )
            else:
                user.socket_id = sid
                user.connected = True

            try:
                room = await Room.get_by_channel_id(session, auth.channel_id)
            except NoResultFound:
                room = await Room.create(session, channel_id=auth.channel_id)
            room.add_user(user)

            await session.commit()

        await self.save_session(sid, {"user_id": user.id})

        return True

    async def on_disconnect(self, sid: str) -> None:
        user_id = (await self.get_session(sid))["user_id"]

        async with Session() as session:
            user = await User.get(session, user_id)
            user.connected = False
            await session.commit()
