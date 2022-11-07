from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config


@Client.on_message(filters.private & filters.command(["broadcast"]) & \
    filters.reply & filters.user(int(config("OWNER_ID"))))
def public_message_preview(client: Client, message: Message):
    message.reply_to_message.copy(
        message.chat.id,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "✅ Send",
                    callback_data="send_public_message"
                ),
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel_public_message"
                )
            ]]
        )
    )



@Client.on_callback_query(filters.regex("^(send|cancel)_public_message$"))
def public_message(client: Client, callback_query: CallbackQuery):
    if callback_query.data == "cancel_public_message":
        callback_query.message.edit(
            "❌ Broadcast canceled."
        )
        return
    
    users = User.objects.all()
    for user in users:
        try:
            callback_query.message.copy(
                user.telegram_id,
                reply_markup=None
            )
        except Exception as e:
            # ToDo: handle flood wait error
            print(e)
            continue

    callback_query.message.reply_text(
        "✅ Broadcast sent."
    )
    