import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import save_story_to_db, fetch_saved_stories, delete_story_from_db


class DatabaseFallbackTests(unittest.TestCase):
    def test_story_round_trip_without_mysql(self):
        story_id = save_story_to_db(
            "Test title",
            "A short story body",
            "Fantasy",
            "story",
            42,
        )

        self.assertIsNotNone(story_id)

        stories = fetch_saved_stories(user_id=42)
        self.assertTrue(any(item["id"] == story_id for item in stories))

        deleted = delete_story_from_db(story_id, 42)
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
