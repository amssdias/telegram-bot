import logging
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
VIDEO_URL = "https://framex-dev.wadrid.net/api/video/"

# Logging config
logger = logging.getLogger("telegram-bot-logger")

logger.setLevel(logging.INFO)

# Set the logging format
info_formatter = logging.Formatter("%(levelname)-8s %(asctime)s: %(message)s - %(filename)s: %(lineno)s")
error_formatter = logging.Formatter("%(levelname)-8s %(asctime)s: %(message)s - %(module)s - %(funcName)s - %(lineno)d")

# Create a file handlers
debug_handler = logging.FileHandler('logs/debug.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(info_formatter)

info_handler = logging.FileHandler('logs/info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(info_formatter)

warning_handler = logging.FileHandler('logs/warning.log')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(error_formatter)

error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(error_formatter)

critical_handler = logging.FileHandler('logs/critical.log')
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(error_formatter)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(critical_handler)
