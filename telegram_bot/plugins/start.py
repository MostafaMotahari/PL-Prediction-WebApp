from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


@Client.on_message(filters.private & filters.command(["start"]))
def start(client: Client, message: Message):
    # Send start message
    if len(message.text.split(" ")) == 1:
            message.reply_text(
            "Hi! I'm a bot for @FBI_Coach.\n"
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
    elif message.text.split(" ")[1] == "success":
        message.reply_text(
            "💡 Your prediction has been successfully submitted.\n"
        )

    # Register a user
    try:
        User.objects.get(telegram_id=message.from_user.id)
    except User.DoesNotExist:
        User.objects.create(
            username=message.from_user.first_name,
            telegram_id=message.from_user.id,
            status="banned"
        )