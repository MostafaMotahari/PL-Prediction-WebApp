from datetime import timedelta
from account.models import User
from prediction.models import GWModel
from django.utils import timezone
from config.settings import ALLOWED_HOSTS
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
import secrets


@Client.on_message(filters.private & filters.regex("^⚽️ Predictions 🎲$"))
def prediction_menu(client: Client, message: Message):
    gameweek = GWModel.objects.get(enabled=True)
    if not gameweek or gameweek.deadline - timedelta(minutes=30) < timezone.now():
        message.reply_text(
            "No prediction available at the moment."
            "It may be because the deadline has passed or the prediction is not yet available."
            "Please wait and try again later."
        )
        return

    user = User.objects.get(telegram_id=message.from_user.id)

    if config("BOT_PREDICTION_MODE") == "ON":
        if user.phone_number:
            if not user.predictions.filter(GW__finished=False).exists():
                # Here we should send the prediction WebApp.
                prediction_token = secrets.token_urlsafe(32)
                user = User.objects.get(telegram_id=message.from_user.id)
                user.prediction_token = prediction_token
                user.token_expiry = timezone.now() + timezone.timedelta(minutes=30)
                user.save()

                message.reply_text(
                    "Here is your prediction token:"
                    "\nNote that this token will expire in 30 minutes.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="🔗 Prediction Token 🔗",
                            url=f"http://{ALLOWED_HOSTS[0]}/prediction/{prediction_token}"
                        )]
                    ])
                )

                return 0

            else:
                message.reply_text(
                    "🫠 You have already predicted this week's fixtures."
                )

                return 0
        
        message.reply_text(
            "❌ First, you need to verify your phone number."
            "For this, you can use the **📱 Veify Phone Number** button in the main menu."
        )
        return

    message.reply_text(
        "❌ Predictions are currently disabled."
    )
    