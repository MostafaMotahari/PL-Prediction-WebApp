from account.models import User
from pyrogram import filters
from decouple import config


power_mode_filter = filters.create(
    lambda _, __, query: config("BOT_POWER_MODE") == "ON"
)

def admin_filter(_, __):
    try:
        return True if User.objects.get(telegram_id=__.from_user.id).status == "admin" else False
    except:
        return False

admin_filter = filters.create(admin_filter)

banned_filter = filters.create(
    lambda _, __, message: User.objects.get(telegram_id=message.from_user.id).status != "banned"
)