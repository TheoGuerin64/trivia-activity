import aiohttp

from .exceptions import APIError


async def token(client_id: str, client_secret: str, code: str) -> dict:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post("https://discord.com/api/oauth2/token", data=data) as response:
            if response.status != 200:
                raise APIError("Failed to get token")
            return await response.json()


async def me(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://discord.com/api/users/@me") as response:
            if response.status != 200:
                raise APIError("Failed to get me")
            return await response.json()
