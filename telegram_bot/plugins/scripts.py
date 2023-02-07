from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from custom_filters import admin_filter
from utils.scripts import get_player_csv


@Client.on_message(filters.private & admin_filter)
def get_player_csv_file(client: Client, message: Message):
    message.reply_text("Please wait ...")
    get_player_csv()

