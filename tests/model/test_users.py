import json
import redis
import unittest
from unittest.mock import MagicMock, patch


from model.users import Users


class TestUsers(unittest.TestCase):
    
    def setUp(self):
        self.redis_mock = MagicMock(spec=redis.Redis)
        self.users = Users()
        self.users.redis_client = self.redis_mock
        return super().setUp()

    @patch("model.users.redis.Redis", return_value=True)
    def test_init(self, mock_redis):
        host = 'my-host'
        port = 1234

        users = Users(host=host, port=port)

        mock_redis.assert_called_once_with(host=host, port=port)
        self.assertEqual(users.redis_client, mock_redis.return_value)


    def test_db_inital_variables(self):
        db_initial_variables = self.users.__dict__.keys()
        self.assertIn("redis_client", db_initial_variables)

        self.assertIsInstance(self.users.redis_client, redis.Redis)

    def test_user_exists(self):
        self.redis_mock.exists.return_value = True
        result = self.users.user_exists(chat_id=123)
        self.assertTrue(result)

    def test_user_nonexists(self):
        self.redis_mock.exists.return_value = False
        result = self.users.user_exists(chat_id=123)
        self.assertFalse(result)

    def test_get_user_info(self):
        self.redis_mock.exists.return_value = True

        user_info = {"min_frame": 100, "max_frame": 200, "current_frame": 150}

        self.redis_mock.get.return_value = json.dumps(user_info)
        result = self.users.get_user_info(chat_id=123)
        self.assertDictEqual(result, user_info)

    def test_get_nonexistent_user_info(self):
        self.redis_mock.exists.return_value = False
        result = self.users.get_user_info(chat_id=123)
        self.assertFalse(result)

    def test_create_user(self):
        self.redis_mock.exists.return_value = False
        max_frame = 100
        result = self.users.create_user(chat_id=123, max_frame=max_frame)

        expected = {
            "current_frame": max_frame // 2,
            "min_frame": 0,
            "max_frame": max_frame,
        }

        self.assertDictEqual(result, expected)

    def test_create_existing_user(self):
        self.redis_mock.exists.return_value = True
        result = self.users.create_user(chat_id=123, max_frame=100)

        self.assertFalse(result)

    def test_update_user(self):
        self.redis_mock.exists.return_value = False
        new_frames = {"current_frame": 150, "min_frame": 100, "max_frame": 200}
        result = self.users.update_user(chat_id=123, user_new_frames=new_frames)
        self.assertTrue(result)

    def test_update_nonexistent_user(self):
        self.redis_mock.exists.return_value = False
        new_frames = {"current_frame": 150, "min_frame": 100, "max_frame": 200}
        result = self.users.update_user(chat_id=123, user_new_frames=new_frames)
        self.assertTrue(result)

    def test_delete_user(self):
        self.redis_mock.delete.return_value = 1
        self.assertTrue(self.users.delete_user(chat_id=123))
    
    def test_delete_nonexistent_user(self):
        self.redis_mock.delete.return_value = 0
        self.assertFalse(self.users.delete_user(chat_id=123))
