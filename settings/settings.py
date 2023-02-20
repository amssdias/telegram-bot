import logging
import os

from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
VIDEO_URL = "https://framex-dev.wadrid.net/api/video/"

DEBUG = os.environ.get("DEBUG", False)

# Logging config
logger = logging.getLogger("telegram-bot-logger")
logger.setLevel(logging.CRITICAL)
formatter = logging.Formatter("%(levelname)-8s %(asctime)s: %(message)s - %(module)s - %(funcName)s - %(lineno)d")
logging.basicConfig(format="%(levelname)-8s %(asctime)s: %(message)s - %(module)s - %(funcName)s - %(lineno)d")

# Sentry config for logging
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.INFO  # Send errors as events
)
sentry_sdk.init(
    dsn=os.environ.get("DSN", ""),

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


if DEBUG:
    from .local_settings import *
