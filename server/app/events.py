from pydantic import ValidationError
from socketio import AsyncNamespace
from sqlalchemy.exc import NoResultFound

from .api import APIError, discord
from .db import Session
from .db.schemas import Room, RoomSettings, RoomState, RoomUser, User
from .models import Auth, Settings
from .session import UserData, get_user_data, save_user_data
from .settings import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET


class Events(AsyncNamespace):
    async def on_connect(self, sid: str, environ: dict[str, str], raw_auth: dict[str, str]) -> None:
        try:
            auth = Auth.model_validate(raw_auth)
            token = await discord.token(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, auth.code)
            me = await discord.me(token["access_token"])
        except (ValidationError, APIError) as error:
            raise ConnectionRefusedError("Invalid auth") from error

        async with Session() as session:
            try:
                user = await User.get_by_discord_id(session, int(me["id"]))
            except NoResultFound:
                user = User(int(me["id"]))
                session.add(user)

            try:
                room = await Room.get_by_channel_id(session, auth.channel_id)
            except NoResultFound:
                room = Room(auth.channel_id, user.id)
                session.add(room)

            await session.commit()

            try:
                room_settings = await RoomSettings.get(session, room.id)
            except NoResultFound:
                room_settings = RoomSettings(room.id)
                session.add(room_settings)
            else:
                await self.emit("settings_update", room_settings.data(), to=sid)

            try:
                room_user = await RoomUser.get(session, user.id, room.id)
            except NoResultFound:
                room_user = RoomUser(room.id, user.id, sid)
                session.add(room_user)
            else:
                room_user.socket_id = sid
                room_user.connected = True

            await session.commit()

            user_data = {
                "is_leader": await room_user.is_leader(),
            }
            await self.emit("user_data", user_data, to=sid)

        await self.enter_room(sid, str(room.id))
        await save_user_data(self, sid, UserData(user.id, room.id))

    async def on_disconnect(self, sid: str) -> None:
        user_id, room_id = await get_user_data(self, sid)

        async with Session() as session:
            room_user = await RoomUser.get(session, user_id, room_id)
            room = await room_user.room
            connected_room_users = await room.connected_room_users()

            if len(connected_room_users) == 1:
                await session.delete(room)
            else:
                if await room_user.is_leader():
                    await room.change_leader()
                    leader = await RoomUser.get(session, room.leader_id, room.id)
                    await self.emit("user_data", {"is_leader": True}, to=leader.socket_id)

                match room.state:
                    case RoomState.LOBBY:
                        await session.delete(room_user)
                    case RoomState.PLAYING:
                        room_user.connected = False

            await session.commit()

    async def on_settings_update(self, sid: str, raw_settings: dict[str, str]) -> None:
        user_id, room_id = await get_user_data(self, sid)

        async with Session() as session:
            room_user = await RoomUser.get(session, user_id, room_id)
            if not await room_user.is_leader():
                return

            try:
                settings = Settings.model_validate(raw_settings)
            except ValidationError:
                await self.emit("error", "invalid settings", to=sid)
                return

            room = await room_user.room
            room_settings = await room.settings
            if settings.round_count is not None:
                room_settings.round_count = settings.round_count
            if settings.difficulty is not None:
                room_settings.difficulty = settings.difficulty

            await session.commit()

            await self.emit(
                "settings_update", room_settings.data(), room=str(room_user.room_id), skip_sid=sid
            )
