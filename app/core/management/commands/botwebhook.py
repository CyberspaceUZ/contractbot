from django.core.management import BaseCommand
import os

from telegram.ext import Updater
from bot.main import init_dispatcher


class Command(BaseCommand):
    help = "run bot pooling for development only"

    def add_arguments(self, parser):
        parser.add_argument(
            "--token",
            action="store",
            default=os.environ.get("BOT_TOKEN"),
            help="Telegram bot token (default from env BOT_TOKEN)",
        )
        parser.add_argument(
            "--port",
            action="store",
            default=os.environ.get("BOT_PORT", 8888),
        )

    def handle(self, *args, **options):
        token = options["token"]
        port = options["port"]
        updater = Updater(token)
        init_dispatcher(updater)
        updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
        updater.bot.set_webhook(
            os.environ.get("BOT_WEBHOOK_URL", "https:test1.artelgroup.org/") + token
        )
        updater.idle()
