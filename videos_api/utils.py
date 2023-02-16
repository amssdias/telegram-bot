from typing import Dict, Optional
import requests


def get_video_info(url: str) -> Optional[Dict]:
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()[0]

    return None
