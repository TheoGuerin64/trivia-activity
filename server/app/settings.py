import os


def get_env(key: str, default: str | None = None) -> str:
    value = os.environ.get(key, default=default)
    assert value is not None, f"{key} environment variable is not set."
    return value


DEV = get_env("DEV", "false").lower() in ("true", "1")

DISCORD_CLIENT_ID = get_env("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = get_env("DISCORD_CLIENT_SECRET")
