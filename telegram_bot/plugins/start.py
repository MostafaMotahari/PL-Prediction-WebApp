from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


@Client.on_message(filters.private & filters.command(["start"]))
def start(client: Client, message: Message):
    message.reply_text(
        "Hi! I'm a bot created by @FBI_Coach.\n"
        "I'm created by @Mousiol.\n"
        "I'm a bot that can help you to get the latest stats from the Fantasy Premier League.\n"
        "You can use /help to get the list of commands.\n",
        
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("📊 Stats"), KeyboardButton("⚽️ Predictions 🎲")],
                [KeyboardButton("👤 Profile")],
                [KeyboardButton("📱 Verify Phone Number", True)],
            ],
            resize_keyboard=True
        )
    )

    # Register a user
    if User.objects.filter(telegram_id=message.from_user.id) is None:
        User.objects.create(telegram_id=message.from_user.id)