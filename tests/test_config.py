import os
import tempfile
import unittest
from pathlib import Path

from config import get_google_api_key


class ConfigTests(unittest.TestCase):
    def test_reads_key_from_env(self):
        os.environ["GOOGLE_API_KEY"] = "test-key"
        self.assertEqual(get_google_api_key(), "test-key")

    def test_reads_key_from_gemini_env_name(self):
        os.environ.pop("GOOGLE_API_KEY", None)
        os.environ["GEMINI_API_KEY"] = "gemini-test-key"
        self.assertEqual(get_google_api_key(), "gemini-test-key")


if __name__ == "__main__":
    unittest.main()
