import json

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""

    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string

    # (see webappbot.html)

    data = json.loads(update.effective_message.web_app_data.data)

    await update.message.reply_html(
        text="You just open the webapp with data: {}".format(data["msg"]),
        reply_markup=ReplyKeyboardRemove(),
    )
