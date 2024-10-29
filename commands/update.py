import json

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from config import DB_PATH
from helper.async_sqlite import DB


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""

    message = update.effective_message
    if not message or not message.web_app_data:
        return

    data = json.loads(message.web_app_data.data or "{}")
    match data.get("action", ""):
        case "send_back_image":
            img_id = data.get("image_id")
            if not img_id:
                return

            db = DB(DB_PATH)
            img_path = await db.get_image_path(img_id)
            if not img_path:
                await update.message.reply_text(  # type: ignore
                    "We can't find the image, sorry.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                return

            await update.message.reply_text(  # type: ignore
                "Ok, here's your image.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await update.message.reply_photo(img_path)  # type: ignore
