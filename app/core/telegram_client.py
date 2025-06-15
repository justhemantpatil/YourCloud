from telethon import TelegramClient
from telethon.sessions import StringSession
from app.core import config
import io

async def get_client(session_string=None):
    if session_string:
        client = TelegramClient(StringSession(session_string), config.API_ID, config.API_HASH)
    else:
        client = TelegramClient('anon', config.API_ID, config.API_HASH)
    await client.connect()
    return client