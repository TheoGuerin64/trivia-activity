import aiohttp

from .exceptions import APIError

DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"


async def getToken(client_id: str, client_secret: str, code: str) -> dict:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(DISCORD_TOKEN_URL, data=data) as response:
            if response.status != 200:
                raise APIError("Failed to get token")
            return await response.json()
