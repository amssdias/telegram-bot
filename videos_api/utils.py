import logging
from typing import Dict, Optional
import requests


logger = logging.getLogger("telegram-bot-logger")


def get_video_info(url: str) -> Optional[Dict]:
    response = requests.get(url)

    if response.status_code == 200:
        logger.info(f"Request to {url} successful with response: {response}")
        return response.json()[0]

    logger.error(f"Request to {url} failed with error message: {response.reason}")
    return None
