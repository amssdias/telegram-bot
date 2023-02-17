import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from settings import BOT_TOKEN, VIDEO_URL
from videos_api.rocket_launch import RocketLaunch
from videos_api.utils import get_video_info


class RocketBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode=None)

        rl_info = get_video_info(VIDEO_URL)
        self.rocket = RocketLaunch(frames=rl_info["frames"], url=rl_info["url"])

        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(KeyboardButton("Yes"), KeyboardButton("No"))

        self.min_frame = 0
        self.max_frame = rl_info["frames"]
        self.current_frame = rl_info["frames"] // 2

    def start(self):
        @self.bot.message_handler(commands=["start"])
        def send_welcome(message) -> None:
            first_name = message.from_user.first_name
            self.bot.reply_to(message, f"Hey, {first_name}!")
            self.bot.send_message(
                chat_id=message.chat.id,
                text=f"I need your help to discover the exact frame where a rocket got launched. (You can check it by watching the picture on the top right corner)",
            )

        self.bot.infinity_polling()
