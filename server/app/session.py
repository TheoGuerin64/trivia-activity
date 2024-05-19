from typing import NamedTuple

from engineio import AsyncServer
from socketio import AsyncNamespace


class UserData(NamedTuple):
    user_id: int
    room_id: int


async def save_user_data_session(
    server: AsyncServer | AsyncNamespace, sid: str, data: UserData
) -> None:
    await server.save_session(sid, {"user_data": data})


async def get_user_data_session(server: AsyncServer | AsyncNamespace, sid: str) -> UserData:
    session = await server.get_session(sid)
    return session["user_data"]
