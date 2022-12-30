from account.models import User
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
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
    user = User.objects.get(telegram_id=message.from_user.id)

    try:
        if __.get_chat_member(config("MAIN_CHANNEL"), message.from_user.id):
            if user.status == "banned":
                user.status = "user"
                user.save()
            
            return True
        
    except UserNotParticipant:
        message.reply_text(
            "You are not a member of the main channel. Please join the main channel and try again.",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Join Channel", url=f"https://t.me/{config('MAIN_CHANNEL')}"),
                ],[
                    InlineKeyboardButton("Confirm", url="https://t.me/PLPredictionBot?start")
                ]]
            )
        )
        user.status = "banned"
        user.save()
        return False
        
    except user.DoesNotExist:
        return False

    except Exception as e:
        print(e)
        return False

banned_filter = filters.create(banned_filter)