from typing import NamedTuple, TypeVarTuple

from engineio import AsyncServer
from socketio import AsyncNamespace


class UserData(NamedTuple):
    user_id: int
    room_id: int


Ts = TypeVarTuple("Ts")


async def save_user_data(namespace: AsyncServer | AsyncNamespace, sid: str, data: UserData) -> None:
    await namespace.save_session(sid, {"user_data": data})


async def get_user_data(namespace: AsyncServer | AsyncNamespace, sid: str) -> UserData:
    session = await namespace.get_session(sid)
    return session["user_data"]
