from account.models import User
from pyrogram import filters
from decouple import config


power_mode_filter = filters.create(
    lambda _, __, query: config("BOT_POWER_MODE") == "ON"
)

admin_filter = filters.create(
    lambda _, __, message: User.objects.get(telegram_id=message.from_user.id).status == "admin"
)

banned_filter = filters.create(
    lambda _, __, message: User.objects.get(telegram_id=message.from_user.id).status != "banned"
)