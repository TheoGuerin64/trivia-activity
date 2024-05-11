from engineio import AsyncServer
from socketio import AsyncNamespace


async def save_user_data(
    namespace: AsyncServer | AsyncNamespace, sid: str, user_id: int, room_id: int
) -> None:
    await namespace.save_session(sid, {"user_id": user_id, "room_id": room_id})


async def get_user_data(namespace: AsyncServer | AsyncNamespace, sid: str) -> tuple[int, int]:
    session = await namespace.get_session(sid)
    return session["user_id"], session["room_id"]
