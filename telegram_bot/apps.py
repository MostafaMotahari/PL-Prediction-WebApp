from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        from . import updater_cron
        updater_cron.start_updater_job()