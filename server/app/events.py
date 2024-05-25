from pydantic import ValidationError
from socketio import AsyncNamespace
from sqlalchemy.ext.asyncio import AsyncSession

from .api import APIError, discord, trivia
from .db import Session
from .db.schemas import Room, RoomQuestion, RoomSettings, RoomState, RoomUser, User
from .models import Auth, Settings
from .session import UserData, get_user_data_session, save_user_data_session
from .settings import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET


class Events(AsyncNamespace):
    async def login(self, session: AsyncSession, sid: str, code: str) -> User:
        """Raises `ConnectionRefusedError` if the code is invalid."""
        try:
            token = await discord.token(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, code)
        except APIError as error:
            raise ConnectionRefusedError("Invalid code") from error

        me = await discord.me(token["access_token"])
        user_id = int(me["id"])

        user, _ = await User.get_or_create(session, user_id)
        return user

    async def on_connect(self, sid: str, environ: dict[str, str], raw_auth: dict[str, str]) -> None:
        try:
            auth = Auth.model_validate(raw_auth)
        except ValidationError as error:
            raise ConnectionRefusedError("Invalid auth") from error

        async with Session() as session:
            user = await self.login(session, sid, auth.code)
            room, room_created = await Room.get_or_create(session, user.id, auth.channel_id)
            if not room_created and room.state != RoomState.LOBBY:
                await session.rollback()
                raise ConnectionRefusedError("Room is playing")

            if room_created:
                room_settings = RoomSettings(room.id)
                session.add(room_settings)
                await session.flush()
            else:
                room_settings = await room.settings
                await self.emit("settings_update", room_settings.data(), to=sid)

            await user.connect(session, room, sid)
            await self.enter_room(sid, str(room.id))
            if room_created:
                await self.emit("user_data", {"is_leader": True}, to=sid)

            await session.commit()

        await save_user_data_session(self, sid, UserData(user.id, room.id))

    async def on_disconnect(self, sid: str) -> None:
        user_id, room_id = await get_user_data_session(self, sid)
        async with Session() as session:
            room_user = await RoomUser.get(session, user_id, room_id)
            room = await room_user.room

            if len(await room.connected_room_users()) == 1:
                await session.delete(room)
            else:
                if await room_user.is_leader():
                    leader = await room.change_leader()
                    await self.emit("user_data", {"is_leader": True}, to=leader.socket_id)

                match room.state:
                    case RoomState.LOBBY:
                        await session.delete(room_user)
                    case RoomState.PLAYING:
                        room_user.connected = False

            await session.commit()

    async def on_settings_update(self, sid: str, raw_settings: dict[str, str]) -> None:
        try:
            settings = Settings.model_validate(raw_settings)
        except ValidationError:
            await self.emit("error", "invalid settings", to=sid)
            return

        user_id, room_id = await get_user_data_session(self, sid)
        async with Session() as session:
            room_user = await RoomUser.get(session, user_id, room_id)
            if not await room_user.is_leader():
                return

            room = await room_user.room
            if room.state != RoomState.LOBBY:
                return

            room_settings = await room.settings
            room_settings.round_count = settings.round_count
            room_settings.difficulty = settings.difficulty
            room_settings.category = settings.category

            await session.commit()

        await self.emit("settings_update", raw_settings, room=str(room.id), skip_sid=sid)

    async def on_start_game(self, sid: str) -> None:
        user_id, room_id = await get_user_data_session(self, sid)

        async with Session() as session:
            room_user = await RoomUser.get(session, user_id, room_id)
            if not await room_user.is_leader():
                return

            room = await room_user.room
            if room.state != RoomState.LOBBY:
                return

            room.state = RoomState.PLAYING
            await session.commit()

            await self.emit("start_game", room=str(room_user.room_id))

            room_settings = await room.settings
            question = await trivia.question(room_settings.category, room_settings.difficulty)

            room_question = RoomQuestion.from_model(room.id, question)
            session.add(room_question)

            await session.commit()

            await self.emit("question", room_question.to_client(), room=str(room.id))
