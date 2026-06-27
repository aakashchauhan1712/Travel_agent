import os
from dotenv import load_dotenv

load_dotenv()


def get_google_api_key():
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if key:
        return key.strip().strip('"').strip("'")
    return None
