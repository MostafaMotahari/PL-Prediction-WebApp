from email import message
from email.message import Message
from account.models import User
from pyrogram import filters
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
        return True if User.objects.get(telegram_id=message.from_user.id).status == "banned" else False
    except:
        return False

banned_filter = filters.create(banned_filter)