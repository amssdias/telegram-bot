import telebot
import unittest
from unittest.mock import MagicMock, patch

from bot.rocket_bot import RocketBot


class TestRocketBot(unittest.TestCase):
    @patch("bot.rocket_bot.get_video_info")
    def setUp(self, mock_get_video_info):
        self.mock_telebot = MagicMock(spec=telebot.TeleBot)
        with patch("bot.rocket_bot.Users"):
            self.rocket_bot = RocketBot(token=123)

        # Mock get_video_info
        video_info = {"frames": 60000, "url": "http://fake-url.com"}
        mock_get_video_info.return_value = video_info

        self.rocket_bot.bot = self.mock_telebot
        return super().setUp()

    @patch("bot.rocket_bot.get_video_info")
    @patch("bot.rocket_bot.Users", return_value=MagicMock())
    @patch("bot.rocket_bot.RocketLaunchAPI")
    def test_init(self, mock_rocket, mock_users, mock_get_video_info):
        token = "my-token"

        # Mock telebot api
        bot_mock = MagicMock()
        telebot.TeleBot = MagicMock(return_value=bot_mock)

        # Mock get_video_info
        video_info = {"frames": 60000, "url": "http://fake-url.com"}
        mock_get_video_info.return_value = video_info

        with patch("bot.rocket_bot.VIDEO_URL", "http://example.com/"):
            bot = RocketBot(token)

        telebot.TeleBot.assert_called_once_with(token, parse_mode=None)
        mock_users.assert_called_once()
        mock_get_video_info.assert_called_once_with("http://example.com/")
        mock_rocket.assert_called_once_with(
            frames=video_info["frames"], url=video_info["url"]
        )
        self.assertEqual(bot.db, mock_users.return_value)
        self.assertEqual(bot.bot, bot_mock)

    def test_send_welcome(self):
        message_mock = MagicMock()
        message_mock.chat.id = 1234
        message_mock.from_user.first_name = "John"

        self.rocket_bot.db.user_exists = MagicMock(return_value=False)
        user_frames = {"current_frame": 150, "min_frame": 100, "max_frame": 200}
        self.rocket_bot.db.create_user = MagicMock(return_value=user_frames)

        self.rocket_bot.bot.reply_to = MagicMock()
        self.rocket_bot.bot.send_message = MagicMock()

        self.rocket_bot.send_rocket_image = MagicMock()

        self.rocket_bot.send_welcome(message=message_mock)

        self.rocket_bot.db.user_exists.assert_called_once_with(message_mock.chat.id)
        self.rocket_bot.db.create_user.assert_called_once_with(
            chat_id=message_mock.chat.id, max_frame=self.rocket_bot.rocket.frames
        )
        self.rocket_bot.bot.reply_to.assert_called_once_with(
            message_mock, f"Hey, {message_mock.from_user.first_name}!"
        )
        self.rocket_bot.bot.send_message.assert_called_once_with(
            chat_id=message_mock.chat.id,
            text="I need your help to discover the exact frame where a rocket got launched. (You can check it by watching the picture in the top right corner)",
        )
        self.rocket_bot.send_rocket_image.assert_called_once_with(
            chat_id=1234, current_frame=user_frames["current_frame"]
        )

    def test_send_welcome_existing_user(self):
        message_mock = MagicMock()
        message_mock.chat.id = 1234
        message_mock.from_user.first_name = "John"

        self.rocket_bot.db.user_exists = MagicMock(return_value=True)
        user_frames = {"current_frame": 150, "min_frame": 100, "max_frame": 200}
        self.rocket_bot.db.get_user_info = MagicMock(return_value=user_frames)

        self.rocket_bot.bot.send_message = MagicMock()

        self.rocket_bot.send_rocket_image = MagicMock()

        self.rocket_bot.send_welcome(message=message_mock)

        self.rocket_bot.db.user_exists.assert_called_once_with(message_mock.chat.id)
        self.rocket_bot.db.get_user_info.assert_called_once_with(message_mock.chat.id)

        self.assertEqual(self.rocket_bot.bot.send_message.call_count, 2)

    def test_restart(self):
        message_mock = MagicMock()
        message_mock.chat.id = 1234

        self.rocket_bot.db.delete_user = MagicMock()
        self.rocket_bot.bot.send_message = MagicMock()

        self.rocket_bot.restart(message_mock)

        self.rocket_bot.db.delete_user.assert_called_once_with(message_mock.chat.id)
        self.rocket_bot.bot.send_message.assert_called_once_with(
            chat_id=message_mock.chat.id, text="Great. To start again, type /start."
        )

    def test_proccess_answer(self):
        message_mock = MagicMock()
        message_mock.chat.id = 1234

        self.rocket_bot.db.user_exists = MagicMock(return_value=True)

        user_frames = {"current_frame": 50, "min_frame": 0, "max_frame": 100}
        self.rocket_bot.db.get_user_info = MagicMock(return_value=user_frames)

        self.rocket_bot.found_frame = MagicMock(return_value=False)

        self.rocket_bot.update_user_frames = MagicMock(
            return_value={"current_frame": 50}
        )
        self.rocket_bot.send_rocket_image = MagicMock()

        for user_message in ["yes", "y", "no", "n"]:
            message_mock.text = user_message

            self.rocket_bot.process_answer(message_mock)

            self.rocket_bot.db.user_exists.assert_called_with(
                chat_id=message_mock.chat.id
            )
            self.rocket_bot.db.get_user_info.assert_called_with(
                chat_id=message_mock.chat.id
            )

            self.rocket_bot.found_frame.assert_called_with(user_frames)

            self.rocket_bot.update_user_frames.assert_called_with(
                chat_id=message_mock.chat.id,
                user_frames=user_frames,
                backwards=True if user_message in ["yes", "y"] else False,
            )

            self.rocket_bot.send_rocket_image.assert_called_with(
                chat_id=message_mock.chat.id,
                current_frame=self.rocket_bot.update_user_frames.return_value[
                    "current_frame"
                ],
            )

    def test_process_answer_nonexisting_user(self):
        message_mock = MagicMock()
        message_mock.chat.id = 1234

        self.rocket_bot.db.user_exists = MagicMock(return_value=False)
        self.rocket_bot.bot.send_message = MagicMock()

        self.rocket_bot.process_answer(message_mock)

        self.rocket_bot.db.user_exists.assert_called_once_with(
            chat_id=message_mock.chat.id
        )
        self.rocket_bot.bot.send_message.assert_called_with(
            chat_id=message_mock.chat.id, text="To start, type /start."
        )

    def test_process_answer_found_frame(self):
        message_mock = MagicMock()
        message_mock.chat.id = 1234

        self.rocket_bot.db.user_exists = MagicMock(return_value=True)

        user_frames = {"current_frame": 50, "min_frame": 0, "max_frame": 100}
        self.rocket_bot.db.get_user_info = MagicMock(return_value=user_frames)

        self.rocket_bot.found_frame = MagicMock(return_value=True)
        self.rocket_bot.find_frame_and_send_message = MagicMock()
        self.rocket_bot.db.delete_user = MagicMock()

        for user_message in ["yes", "y", "no", "n"]:
            message_mock.text = user_message

            self.rocket_bot.process_answer(message_mock)

            self.rocket_bot.db.user_exists.assert_called_with(
                chat_id=message_mock.chat.id
            )
            self.rocket_bot.db.get_user_info.assert_called_with(
                chat_id=message_mock.chat.id
            )

            self.rocket_bot.found_frame.assert_called_with(user_frames)
            self.rocket_bot.find_frame_and_send_message.assert_called_with(
                chat_id=message_mock.chat.id,
                user_frames=user_frames,
                user_message=user_message.upper(),
            )
            self.rocket_bot.db.delete_user.assert_called_with(message_mock.chat.id)

    def test_update_user_frames_backwards(self):
        chat_id = 1234

        self.rocket_bot.db.update_user = MagicMock()

        user_frames = {
            "current_frame": 150,
            "min_frame": 100,
            "max_frame": 200,
        }

        user_frames["max_frame"] = user_frames["current_frame"]
        user_frames["current_frame"] = (
            user_frames["min_frame"] + user_frames["max_frame"]
        ) // 2

        result = self.rocket_bot.update_user_frames(
            chat_id=chat_id, user_frames=user_frames, backwards=True
        )

        self.assertDictEqual(result, user_frames)
        self.rocket_bot.db.update_user.assert_called_once_with(chat_id, result)

    def test_update_user_frames_forward(self):
        chat_id = 1234

        self.rocket_bot.db.update_user = MagicMock()

        user_frames = {
            "current_frame": 150,
            "min_frame": 100,
            "max_frame": 200,
        }

        user_frames["min_frame"] = user_frames["current_frame"]
        user_frames["current_frame"] = (
            user_frames["min_frame"] + user_frames["max_frame"]
        ) // 2

        result = self.rocket_bot.update_user_frames(
            chat_id=chat_id, user_frames=user_frames, backwards=False
        )

        self.assertDictEqual(result, user_frames)
        self.rocket_bot.db.update_user.assert_called_once_with(chat_id, result)

    def test_send_rocket_image(self):
        frames = "b"
        self.rocket_bot.rocket.get_frame = MagicMock(return_value=frames)
        self.rocket_bot.send_rocket_img_message = MagicMock()

        chat_id = 1234
        current_frame = 50
        self.rocket_bot.send_rocket_image(chat_id=chat_id, current_frame=current_frame)

        self.rocket_bot.rocket.get_frame.assert_called_once_with(current_frame)
        self.rocket_bot.send_rocket_img_message.assert_called_once_with(
            img=frames, chat_id=chat_id
        )

    def test_send_rocket_image_no_img(self):
        self.rocket_bot.rocket.get_frame = MagicMock(return_value=False)
        self.rocket_bot.bot.send_message = MagicMock()

        chat_id = 1234
        current_frame = 50
        self.rocket_bot.send_rocket_image(chat_id=chat_id, current_frame=current_frame)

        self.rocket_bot.rocket.get_frame.assert_called_once_with(current_frame)
        self.rocket_bot.bot.send_message.assert_called_once_with(
            chat_id=chat_id, text="Sorry, the image is not available, try again later."
        )

    def test_send_rocket_img_message(self):
        self.rocket_bot.bot.send_photo = MagicMock()
        self.rocket_bot.bot.send_message = MagicMock()

        img = b"image"
        chat_id = 1234
        self.rocket_bot.send_rocket_img_message(img=img, chat_id=chat_id)

        self.rocket_bot.bot.send_photo.assert_called_once()
        self.rocket_bot.bot.send_message.assert_called_once()

    def test_found_frame_current_equal_min(self):
        user_frames = {"current_frame": 0, "min_frame": 0, "max_frame": 100}
        result = self.rocket_bot.found_frame(user_frames)

        self.assertTrue(result)

    def test_found_frame_current_equal_max(self):
        user_frames = {"current_frame": 100, "min_frame": 0, "max_frame": 100}
        result = self.rocket_bot.found_frame(user_frames)

        self.assertTrue(result)

    def test_found_frame_current_not_equal(self):
        user_frames = {"current_frame": 50, "min_frame": 0, "max_frame": 100}
        result = self.rocket_bot.found_frame(user_frames)

        self.assertFalse(result)

    def test_find_frame_and_send_message_min_frame(self):
        self.rocket_bot.bot.send_message = MagicMock()

        chat_id = 1234
        user_frames = {"current_frame": 0, "min_frame": 0, "max_frame": 100}

        for user_message in ["N", "NO"]:
            self.rocket_bot.find_frame_and_send_message(
                chat_id, user_frames, user_message
            )

            self.rocket_bot.bot.send_message.assert_called_with(
                chat_id=chat_id,
                text=f"You found it! The frame is {user_frames['max_frame']}. To do it again type /start.",
            )

    def test_find_frame_and_send_message_max_frame(self):
        self.rocket_bot.bot.send_message = MagicMock()

        chat_id = 1234
        user_frames = {"current_frame": 100, "min_frame": 0, "max_frame": 100}

        self.rocket_bot.find_frame_and_send_message(chat_id, user_frames, "Y")

        self.rocket_bot.bot.send_message.assert_called_with(
            chat_id=chat_id,
            text=f"You found it! The frame is {user_frames['min_frame']}. To do it again type /start.",
        )
