import io
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from settings import VIDEO_URL
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

            img = self.rocket.get_frame(self.current_frame)
            if img:
                self.send_rocket_img(img=img, chat_id=message.chat.id)

        @self.bot.message_handler(func=lambda msg: True)
        def process_answer(message) -> None:
            if (
                self.current_frame + 1 == self.max_frame
                or self.current_frame - 1 == self.min_frame
            ):
                frame = self.max_frame if self.current_frame + 1 == self.max_frame else self.min_frame
                
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"You found it! The frame is {frame}",
                )

                return None

            if message.text.upper() in ["YES", "Y"]:
                # Go back on frames

                self.max_frame = self.current_frame + 1
                self.current_frame = (self.min_frame + self.max_frame) // 2

                img = self.rocket.get_frame(self.current_frame)
                if img:
                    self.send_rocket_img(img=img, chat_id=message.chat.id)

            elif message.text.upper() in ["NO", "N"]:
                # Go front on frames

                self.min_frame = self.current_frame - 1
                self.current_frame = (self.min_frame + self.max_frame) // 2

                img = self.rocket.get_frame(self.current_frame)
                if img:
                    self.send_rocket_img(img=img, chat_id=message.chat.id)

            else:
                self.bot.reply_to(
                    message, "I'm sorry, I didn't understand your response."
                )

        self.bot.infinity_polling()

    def send_rocket_img(self, img, chat_id, text="Did the rocket launched?"):
        photo = io.BytesIO(img)
        self.bot.send_photo(chat_id=chat_id, photo=photo)

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=self.keyboard,
        )
