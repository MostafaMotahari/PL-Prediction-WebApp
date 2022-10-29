from account.models import User
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config


power_mode_filter = filters.create(
    lambda _, __, query: config("BOT_POWER_MODE") == "ON"
)

def admin_filter(_, __, message):
    try:
        return True if User.objects.get(telegram_id=message.from_user.id).status == "admin" else False
    except:
        return False

admin_filter = filters.create(admin_filter)

def banned_filter(_, __, message):
    try:
        user = User.objects.get(telegram_id=message.from_user.id)
        # Check if the user is a member of the main channel
        for member in __.get_chat_members(config("MAIN_CHANNEL")):
            if member.user.id == user.telegram_id:
                if user.status == "banned":
                    user.status = "user"
                break
        else:
            message.reply_text(
                "You are not a member of the main channel. Please join the main channel and try again.",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("Join Channel", url="https://t.me/your_channel")
                    ]]
                )
            )
            user.status = "banned"
        
        user.save()
        return False if user.status == "banned" else True
    except:
        return False

banned_filter = filters.create(banned_filter)