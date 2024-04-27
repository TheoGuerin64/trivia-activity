import socketio
from aiohttp import web

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.event
def connect(sid: str, environ: dict):
    print("connect ", type(environ), sio.transport(sid))


@sio.event
async def message(sid: str, data: str):
    print("message ", data)


@sio.event
def disconnect(sid: str):
    print("disconnect ", sid)


if __name__ == "__main__":
    web.run_app(app, port=3000)
