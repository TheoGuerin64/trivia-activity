import uvicorn

from . import schemas  # noqa: F401

uvicorn.run("app:app", ws_max_size=2**12, host="0.0.0.0", port=3000, reload=__debug__)
