import io
from typing import Dict
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from model.users import Users
from settings.settings import VIDEO_URL
from videos_api.rocket_launch import RocketLaunchAPI
from videos_api.utils import get_video_info


class RocketBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode=None)
        self.db = Users()

        rl_info = get_video_info(VIDEO_URL)
        if rl_info:
            self.rocket = RocketLaunchAPI(frames=rl_info["frames"], url=rl_info["url"])

        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(KeyboardButton("Yes"), KeyboardButton("No"))

    def start(self):
        @self.bot.message_handler(commands=["start"])
        def send_welcome(message) -> None:
            self.send_welcome(message)

        @self.bot.message_handler(commands=["restart"])
        def restart(message) -> None:
            self.restart(message)

        @self.bot.message_handler(func=lambda msg: True)
        def process_answer(message) -> None:
            self.process_answer(message)

        self.bot.infinity_polling()

    def send_welcome(self, message) -> None:
        chat_id = message.chat.id
        first_name = message.from_user.first_name

        # Check if user exists, if yes, ask him to help you again, else save user info
        if self.db.user_exists(chat_id):
            user_frames_info = self.db.get_user_info(chat_id)
            self.bot.send_message(
                chat_id=chat_id,
                text=f"Hey {first_name}! Can you continue helping me discover when was the exact frame a rocket launched? (You can check it by watching the picture in the top right corner)",
            )
            self.bot.send_message(
                chat_id=chat_id,
                text="If you would like to restart from beginning just type /restart.",
            )

        else:
            user_frames_info = self.db.create_user(
                chat_id=chat_id, max_frame=self.rocket.frames
            )

            self.bot.reply_to(message, f"Hey, {first_name}!")
            self.bot.send_message(
                chat_id=chat_id,
                text="I need your help to discover the exact frame where a rocket got launched. (You can check it by watching the picture in the top right corner)",
            )

        self.send_rocket_image(
            chat_id=chat_id, current_frame=user_frames_info["current_frame"]
        )

    def restart(self, message) -> None:
        chat_id = message.chat.id
        self.db.delete_user(chat_id)
        self.bot.send_message(
            chat_id=chat_id,
            text="Great. To start again, type /start.",
        )

    def process_answer(self, message) -> None:
        chat_id = message.chat.id

        if not self.db.user_exists(chat_id=chat_id):
            self.bot.send_message(
                chat_id=chat_id,
                text="To start, type /start.",
            )
            return None

        user_frames = self.db.get_user_info(chat_id=chat_id)
        user_message = message.text.upper()

        if self.found_frame(user_frames) and user_message in ["YES", "Y", "NO", "N"]:
            self.find_frame_and_send_message(
                chat_id=chat_id, user_frames=user_frames, user_message=user_message
            )
            self.db.delete_user(chat_id)
            return None

        if user_message in ["YES", "Y", "NO", "N"]:
            # Go backwards frames if True
            backwards = True if user_message in ["YES", "Y"] else False
            new_frames = self.update_user_frames(
                chat_id=chat_id, user_frames=user_frames, backwards=backwards
            )

            # Send rocket image with new frames
            self.send_rocket_image(
                chat_id=chat_id, current_frame=new_frames["current_frame"]
            )

        else:
            self.bot.reply_to(
                message,
                "I'm sorry, I didn't understand your response. Just type 'Yes' or 'No'.",
            )

    def update_user_frames(
        self, chat_id: int, user_frames: Dict, backwards: bool
    ) -> Dict:
        """Recalculate user frames and save them back on the current user."""

        if backwards:
            user_frames["max_frame"] = user_frames["current_frame"] - 1
        else:
            user_frames["min_frame"] = user_frames["current_frame"] + 1

        user_frames["current_frame"] = (
            user_frames["min_frame"] + user_frames["max_frame"]
        ) // 2

        self.db.update_user(chat_id, user_frames)

        return user_frames

    def send_rocket_image(self, chat_id: int, current_frame: int) -> None:
        img = self.rocket.get_frame(current_frame)
        if img:
            self.send_rocket_img_message(img=img, chat_id=chat_id)
        else:
            self.bot.send_message(
                chat_id=chat_id,
                text="Sorry, the image is not available, try again later.",
            )

    def send_rocket_img_message(
        self, img, chat_id: int, text="Did the rocket launch?"
    ) -> None:
        photo = io.BytesIO(img)
        self.bot.send_photo(chat_id=chat_id, photo=photo)

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=self.keyboard,
        )

    def found_frame(self, user_frames: Dict) -> bool:
        """Verify if user found the correct frame."""
        return (
            user_frames["current_frame"] == user_frames["max_frame"]
            or user_frames["current_frame"] == user_frames["min_frame"]
        )

    def find_frame_and_send_message(
        self, chat_id: int, user_frames: Dict, user_message=str
    ) -> None:
        frame = (
            user_frames["max_frame"]
            if user_frames["current_frame"] == user_frames["min_frame"]
            and user_message in ["NO", "N"]
            else user_frames["min_frame"]
        )

        self.bot.send_message(
            chat_id=chat_id,
            text=f"You found it! The frame is {frame}. To do it again type /start.",
        )
