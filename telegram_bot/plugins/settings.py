import os

from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config

from telegram_bot.plugins.custom_filters import admin_filter
from telegram_bot.plugins.fixtures_updater import need_to_update_fixtures

# Message templates
SETTING_MESSAGE = """
Bot settings:
Power mode: {}
Prediction mode: {}
Need to update fixtures: {}

- Users: {}
- Admins: {}
- Banned: {}
"""

def inline_keyboard_maker(power_mode, prediction_mode, update_fixture=False):
    keyboard = [
        [InlineKeyboardButton(
            "⚡️Power mode⚡️",
            callback_data=power_mode
        )],
        [InlineKeyboardButton(
            "🔮Prediction mode🔮",
            callback_data=prediction_mode
        )]
    ]

    if update_fixture:
        keyboard.append(
            [InlineKeyboardButton(
                "🔄Update Fixtures🔄",
                callback_data="update_fixture"
            )]
        )

    return InlineKeyboardMarkup(keyboard)


@Client.on_message(admin_filter & filters.private & filters.command(["settings"]))
def settings(client: Client, message: Message):
    message.reply_text(
        SETTING_MESSAGE.format(
            "⬜️🟩" if config("BOT_POWER_MODE") == "ON" else "🟥⬜️",
            "🟥⬜️" if config("BOT_PREDICTION_MODE") == "OFF" else "⬜️🟩",
            "⬜️🟩" if need_to_update_fixtures() else "🟥⬜️",
            len(User.objects.all()),
            len(User.objects.filter(status="admin").all()),
            len(User.objects.filter(status="banned").all()),
        ),
        reply_markup=inline_keyboard_maker(
            "power_off" if config("BOT_POWER_MODE") == "ON" else "power_on",
            "prediction_off" if config("BOT_PREDICTION_MODE") == "OFF" else "prediction_on",
            need_to_update_fixtures()
        )  
    )

# Power mode snippet
@Client.on_callback_query(filters.regex("power_(on|off)"))
def power_mode(client: Client, callback_query):
    if callback_query.data == "power_on":
        # Power mode is off, turn it on
        os.environ["BOT_POWER_MODE"] = "ON"
    else:
        # Power mode is on, turn it off
        os.environ["BOT_POWER_MODE"] = "OFF"

    callback_query.edit_message_text(
        SETTING_MESSAGE.format(
            "🟥⬜️" if config("BOT_POWER_MODE") == "OFF" else "⬜️🟩",
            "🟥⬜️" if config("BOT_PREDICTION_MODE") == "OFF" else "⬜️🟩",
            "⬜️🟩" if need_to_update_fixtures() else "🟥⬜️",
            len(User.objects.all()),
            len(User.objects.filter(status="admin").all()),
            len(User.objects.filter(status="banned").all()),
        ),
        reply_markup=inline_keyboard_maker(
            "power_off" if config("BOT_POWER_MODE") == "ON" else "power_on",
            "prediction_off" if config("BOT_PREDICTION_MODE") == "OFF" else "prediction_on",
            need_to_update_fixtures()
        )
    )


# Prediction mode snippets
@Client.on_callback_query(filters.regex("prediction_(on|off)"))
def prediction_mode(client: Client, callback_query):
    if callback_query.data == "prediction_on":
        # Prediction mode is off, turn it on
        os.environ["BOT_PREDICTION_MODE"] = "ON"
    else:
        # Prediction mode is on, turn it off
        os.environ["BOT_PREDICTION_MODE"] = "OFF"

    callback_query.edit_message_text(
        SETTING_MESSAGE.format(
            "🟥⬜️" if config("BOT_POWER_MODE") == "OFF" else "⬜️🟩",
            "🟥⬜️" if config("BOT_PREDICTION_MODE") == "OFF" else "⬜️🟩",
            "⬜️🟩" if need_to_update_fixtures() else "🟥⬜️",
            len(User.objects.all()),
            len(User.objects.filter(status="admin").all()),
            len(User.objects.filter(status="banned").all()),
        ),
        reply_markup=inline_keyboard_maker(
            "power_off" if config("BOT_POWER_MODE") == "ON" else "power_on",
            "prediction_off" if config("BOT_PREDICTION_MODE") == "OFF" else "prediction_on",
            need_to_update_fixtures()
        )
    )