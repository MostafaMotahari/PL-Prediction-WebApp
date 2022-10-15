from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from decouple import config


@Client.on_message(filters.private & filters.regex("^⚽️ Predictions 🎲$"))
def prediction_menu(client: Client, message: Message):
    user = User.objects.get(telegram_id=message.from_user.id)

    if config("BOT_PREDICTION_MODE") == "ON":
        if user.phone_number:
            # Here we should send the prediction WebApp.
            message.reply_text(
                "✅ You can now predict the results of the matches."
            )
            return
        
        message.reply_text(
            "❌ First, you need to verify your phone number."
            "For this, you can use the **📱 Veify Phone Number** button in the main menu."
        )
        return

    message.reply_text(
        "❌ Predictions are currently disabled."
    )
    