from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.plugins.custom_filters import banned_filter, power_mode_filter


@Client.on_message(filters.private & filters.regex("^👤 Profile$") \
    & power_mode_filter & banned_filter)
def profile(client: Client, message: Message):
    user = User.objects.get(telegram_id=message.from_user.id)

    message.reply_text(
        "👤 Profile\n"
        f"- User name: {message.from_user.first_name}\n"
        f"- User id: {message.from_user.id}\n"
        f"- Phone number: {user.phone_number}\n"
        f"- Card number: {user.card_number}\n"
        f"- Status: {user.status}\n\n"
        
        "⭐️ Prediction points:\n"
        f"- Weekly points: {user.weekly_prediction_points}\n"
        f"- Monthly points: {user.monthly_prediction_points}\n"
        f"- Total points: {user.total_prediction_points}\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("View History", callback_data="view_history")]]
        )
    )
