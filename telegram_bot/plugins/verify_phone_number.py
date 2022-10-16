from account.models import User
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

# ToDo: add an option to change country code from env file or settings.
@Client.on_message(filters.private & filters.contact)
def verify_phone_number(client: Client, message: Message):

    user = User.objects.get(telegram_id=message.from_user.id)
    if user:
        if user.phone_number:
            message.reply_text(
                "✅ You already have a phone number associated with your account."
            )
            return

        elif message.contact.phone_number.startswith("+98") or message.contact.phone_number.startswith("98"):
            user.phone_number = message.contact.phone_number
            user.save()
            message.reply_text(
                "✅ Your phone number has been successfully verified."
            )
            return

        message.reply_text(
            "❌ You can only use an Iranian phone number."
        )

    else:
        message.reply_text(
            "❌ You don't have an account with us."
        )