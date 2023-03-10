import logging
import json
import redis
from typing import Dict, Union


logger = logging.getLogger("telegram-bot-logger")


class Users:
    def __init__(self, host="localhost", port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def user_exists(self, chat_id: int) -> bool:
        return self.redis_client.exists(chat_id)

    def get_user_info(self, chat_id: int) -> Dict:
        return (
            json.loads(self.redis_client.get(chat_id))
            if self.user_exists(chat_id=chat_id)
            else None
        )

    def create_user(self, chat_id: int, max_frame: int) -> Union[Dict, bool]:
        user_frames_info = {
            "current_frame": max_frame // 2,
            "min_frame": 0,
            "max_frame": max_frame,
        }

        user = (
            self.redis_client.set(chat_id, json.dumps(user_frames_info))
            if not self.user_exists(chat_id=chat_id)
            else False
        )

        if user:
            logger.info(f"User with chat ID: {chat_id} created.")
            return user_frames_info
        else:
            logger.info(f"User with chat ID: {chat_id} already exists.")
            return user

    def update_user(self, chat_id: int, user_new_frames: Dict) -> bool:
        return (
            self.redis_client.set(chat_id, json.dumps(user_new_frames))
            if not self.user_exists(chat_id=chat_id)
            else None
        )

    def delete_user(self, chat_id: int) -> int:
        logger.info(f"User with chat ID: {chat_id} deleted.")
        return self.redis_client.delete(chat_id)
