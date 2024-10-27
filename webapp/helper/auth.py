from init_data_py import InitData
from init_data_py.types import User

from config import BOT_TOKEN


def validate_token(token: str) -> tuple[bool, User | None]:
    if not token.startswith("Telegram-app "):
        return False, None

    init_data = InitData.parse(token.split(" ", 1)[1])
    return init_data.validate(BOT_TOKEN, lifetime=3600), init_data.user
