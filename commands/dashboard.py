from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes


async def imgs_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if not user or not update.message:
        return

    await update.message.reply_text(
        "Click the button below to open your dashboard.",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Open dashboard",
                web_app=WebAppInfo(
                    url="https://vrixnp.tunnel.pyjam.as/",
                ),
            ),
        ),
    )
