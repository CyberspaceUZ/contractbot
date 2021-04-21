from django.core.management import BaseCommand
import os
import logging
from redis import Redis
from redispersistence.persistence import RedisPersistence

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

    def handle(self, *args, **options):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger("bot")
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console)
        token = options["token"]
        redis_instance = Redis(host='localhost', port=6379, db=0)
        persistence = RedisPersistence(redis_instance)
        updater = Updater(token, persistence=persistence)
        init_dispatcher(updater)
        updater.start_polling()
        updater.idle()
