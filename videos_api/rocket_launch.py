import requests


class RocketLaunchAPI:
    def __init__(self, frames, url):
        self.frames = frames
        self.url = url

    def get_frame(self, frame):
        url_formated = f"{self.url}frame/{frame}/"

        response = requests.get(url_formated)
        return response.content if response.status_code == 200 else None
