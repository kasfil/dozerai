import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
MAX_MSG_CHARS = int(os.getenv("MAX_MSG_CHARS", 3000))

BASE_PATH = Path(__file__).parent
GROUP_PATH = Path.joinpath(BASE_PATH, "static", "groups")
IMG_PATH = Path.joinpath(BASE_PATH, "static", "images")

DB_PATH = Path.joinpath(BASE_PATH, "dozer.db")
