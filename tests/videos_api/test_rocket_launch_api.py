import random
import unittest
from unittest.mock import MagicMock, patch

from videos_api.rocket_launch import RocketLaunchAPI


class TestRocketLaunchAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.frames = 10000
        self.url = "http://testing.com/"
        self.api = RocketLaunchAPI(frames=self.frames, url=self.url)
        return super().setUp()

    def test_rocket_launch_api_initial_variables(self):
        rocket_launch_initial_variables = self.api.__dict__.keys()
        self.assertIn("frames", rocket_launch_initial_variables)
        self.assertIn("url", rocket_launch_initial_variables)

        self.assertIsInstance(self.api.frames, int)
        self.assertIsInstance(self.api.url, str)

        self.assertEqual(self.api.frames, self.frames)
        self.assertEqual(self.api.url, self.url)

    def test_get_frame_success(self):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.content = b"fake image data"

        with patch("requests.get", return_value=response_mock):
            frame_data = self.api.get_frame(random.randint(0, self.frames))

        self.assertEqual(frame_data, b"fake image data")

    def test_get_frame_failure(self):
        response_mock = MagicMock()
        response_mock.status_code = 400
        response_mock.content = None

        with patch("requests.get", return_value=response_mock):
            frame_data = self.api.get_frame(random.randint(0, self.frames))

        self.assertIsNone(frame_data)
