import os

from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv("API_HOST", None)
if API_HOST is None:
    raise ValueError("API_HOST is not set")
