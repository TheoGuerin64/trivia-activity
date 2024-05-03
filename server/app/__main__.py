import uvicorn

from .settings import DEV

uvicorn.run("app:app", ws_max_size=2**12, host="0.0.0.0", port=3000, reload=DEV)
