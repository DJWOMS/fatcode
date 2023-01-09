import telegram
from django.conf import settings
from .models import Report
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=Report)
def send_telegram_message(sender, instance, created, **kwargs):
    if not settings.DEBUG:
        message = f'Жалоба от {instance.user}, Проблема: {instance.text}'
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        bot.send_message(
            chat_id=telegram_settings['channel_id'],
            text=message, parse_mode=telegram.ParseMode.HTML
        )
