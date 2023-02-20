import logging
import requests


logger = logging.getLogger("telegram-bot-logger")


class RocketLaunchAPI:
    def __init__(self, frames, url):
        self.frames = frames
        self.url = url

    def get_frame(self, frame):
        url_formated = f"{self.url}frame/{frame}/"

        response = requests.get(url_formated)
        if response.status_code == 200:
            logger.info(f"Request to {url_formated} successful with response: {response.content}")
            return response.content
        else:
            logger.error(f"Request to {url_formated} failed with error message: {response.reason}")
            return None
