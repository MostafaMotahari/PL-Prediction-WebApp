""""This files is the main file of the bot"""
from pyrogram.client import Client
from decouple import config

PLUGINS = dict(root='telegram_bot/plugins')
PROXY = {
    "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
    "hostname": config('PROXY_HOSTNAME'),
    "port": int(config('PROXY_PORT')),
}

app = Client(
    "FplBot",
    api_id=config("API_ID"),
    api_hash=config("API_HASH"),
    bot_token=config("BOT_TOKEN"),
    plugins=PLUGINS,
#    proxy=PROXY,
)
