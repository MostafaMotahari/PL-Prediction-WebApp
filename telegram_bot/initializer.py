""""This files is the main file of the bot"""
import sys

from pyrogram.client import Client
from decouple import config

PLUGINS = dict(root='src/plugins')
PROXY = {
    "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
    "hostname": config('PROXY_HOSTNAME'),
    "port": config('PROXY_PORT'),
}

app = Client(
    "FplBot",
    api_id=config("API_ID"),
    api_hash=config("API_HASH"),
    bot_token=config("BOT_TOKEN"),
    plugins=PLUGINS,
    proxy=PROXY,
)