import os
import sqlite3
import tempfile
import unittest

import main


class AuthStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_users.db")
        main.DB_PATH = self.db_path
        main.init_db()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_verify_user(self):
        user = main.create_user("alice", "alice@example.com", "secret123")
        self.assertEqual(user["username"], "alice")
        self.assertTrue(user["token"])

        verified = main.verify_login("alice", "secret123")
        self.assertTrue(verified)

        wrong_password = main.verify_login("alice", "wrong")
        self.assertFalse(wrong_password)


if __name__ == "__main__":
    unittest.main()
