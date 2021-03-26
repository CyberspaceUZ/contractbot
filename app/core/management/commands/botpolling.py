from django.core.management import BaseCommand
import os

from telegram.ext import Updater
from bot.main import init_dispatcher


class Command(BaseCommand):
    help = 'run bot pooling for development only'

    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            action='store',
            default=os.environ.get('BOT_TOKEN'),
            help='Telegram bot token (default from env BOT_TOKEN)',
        )

    def handle(self, *args, **options):
        token = options['token']
        updater = Updater(token)
        init_dispatcher(updater)
        updater.start_polling()
        updater.idle()
