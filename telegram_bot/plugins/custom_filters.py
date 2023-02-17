from account.models import User
from tournament.models import Tournament
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
    try:
        user = User.objects.get(telegram_id=message.from_user.id)

        if __.get_chat_member(config("MAIN_CHANNEL"), message.from_user.id) and __.get_chat_member("Fpl_Phoenix", message.from_user.id):
            if user.status == "banned":
                user.status = "user"
                user.save()

            return True

    except UserNotParticipant:
        message.reply_text(
            "You are not a member of our channels. Please join the our channels and try again.",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("FBI Coach", url=f"https://t.me/{config('MAIN_CHANNEL')}"),
                ],[
                    InlineKeyboardButton("FPL PHOENIX", url="https://t.me/FPL_PHOENIX")
                ],[
                    InlineKeyboardButton("Confirm", url="https://t.me/PLPredictionBot?start")
                ]]
            )
        )
        user.status = "banned"
        user.save()
        return False

    except Exception as e:
        print(e)
        return False


banned_filter = filters.create(banned_filter)


def is_participant(_, __, query):
    try:
        Tournament.objects.get(pk=query.data.split("-")[2], players__telegram_id=query.from_user.id)
        query.answer("You are already participating in this tournament.")
        return False

    except Tournament.DoesNotExist:
        return True


is_participant_filter = filters.create(is_participant)
