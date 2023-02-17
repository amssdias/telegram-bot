import unittest
from unittest.mock import MagicMock, patch

from videos_api.utils import get_video_info


class TestGetVideo(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://testing.com/"
        return super().setUp()

    def test_get_video_info_success(self):
        response_mock = MagicMock()
        response_mock.status_code = 200
        video_info = {"video_name": "Testing video"}
        response_mock.json = MagicMock(return_value=[video_info])

        with patch("requests.get", return_value=response_mock):
            frame_data = get_video_info(self.url)

        self.assertEqual(frame_data, video_info)
        self.assertIsInstance(frame_data, dict)

    def test_get_video_info_failure(self):
        response_mock = MagicMock()
        response_mock.status_code = 400

        with patch("requests.get", return_value=response_mock):
            frame_data = get_video_info(self.url)

        self.assertIsNone(frame_data)
