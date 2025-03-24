import aiohttp
from aiogram import Bot
from .settings import URLs as URLs_object
from .settings import CHANNELS

URLs = URLs_object()


async def check_is_subscribed(bot: Bot, user_id: int) -> bool:
    statuses = [
        (await bot.get_chat_member(chat_id=channel_id, user_id=user_id)).status
        for channel_id in CHANNELS.keys()
    ]
    return "left" not in statuses


async def add_user(
    id: str, name: str, username: str | None = None
) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        return await session.post(
            URLs.ADD_USER_ENDPOINT,
            json={
                "id": id,
                "name": name,
                "username": username,
            },
        )


async def update_or_add_user(
    id: str, name: str, username: str | None = None, phone_number: str | None = None
) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        return await session.post(
            URLs.UPDATE_OR_ADD_USER_ENDPOINT,
            json={
                "id": id,
                "name": name,
                "username": username,
                "phone_number": phone_number,
            }
        )


async def get_user(user_id: str) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        return await session.get(URLs.get_user_endpoint(user_id))


async def get_users() -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        return await session.get(URLs.USERS_API_ENDPOINT)
