import uvicorn

from . import schemas  # noqa: F401
from .db import Base, engine
from .settings import DEV

Base.metadata.create_all(bind=engine)
uvicorn.run("app:app", ws_max_size=2**12, host="0.0.0.0", port=3000, reload=DEV)
