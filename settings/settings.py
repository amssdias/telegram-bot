import logging
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
VIDEO_URL = "https://framex-dev.wadrid.net/api/video/"

DEBUG = os.environ.get("DEBUG", True)

# Logging config
logger = logging.getLogger("telegram-bot-logger")
logger.setLevel(logging.CRITICAL)
formatter = logging.Formatter("%(levelname)-8s %(asctime)s: %(message)s - %(module)s - %(funcName)s - %(lineno)d")
logging.basicConfig(format="%(levelname)-8s %(asctime)s: %(message)s - %(module)s - %(funcName)s - %(lineno)d")


if DEBUG:
    from .local_settings import *
