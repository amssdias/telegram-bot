import json
from typing import Dict
import redis

class Users:

    def __init__(self, host="localhost", port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def user_exists(self, chat_id: int) -> bool:
        return self.redis_client.exists(chat_id)

    def get_user_info(self, chat_id: int) -> Dict:
        return json.loads(self.redis_client.get(chat_id))

    def create_user(self, chat_id: int, max_frame: int) -> Dict:
        user_frames_info = {
            "current_frame": max_frame // 2,
            "min_frame": 0,
            "max_frame": max_frame,
        }
        self.redis_client.set(chat_id, json.dumps(user_frames_info))
        
        return user_frames_info

    def update_user(self, chat_id: int, user_new_frames: Dict) -> bool:
        return self.redis_client.set(chat_id, json.dumps(user_new_frames))

    def delete_user(self, chat_id: int) -> int:
        return self.redis_client.delete(chat_id)
