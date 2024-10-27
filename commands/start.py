from telegram import Update
from telegram.ext import ContextTypes

from config import DEBUG


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if not user or not update.message:
        return

    reply = """Welcome {name}! 👏
🤖 I am Dozer, Your All-in-One Health, Safety, and Environment Support Bot — designed to streamline HSE reporting, guidance, and support. Here’s what I can do for you:

- /ask - Have a question? just ask!

- /rate - Submit an image for safety rating (0 - 10), and receive recommendations to enhance safety.

- /profile - Get to know your account summary.

- /mytoken - Check your personal reward token.

- /redeem - Exchange tokens for rewards, recognizing your commitment to HSE.
"""  # noqa: E501

    if DEBUG:
        reply += """

<b>-- YOU ARE USING DEVELOPMENT MODE --</b>"""

    await update.message.reply_sticker(
        "CAACAgIAAxkBAAEujvJnFfp3d1fb3XZjZhR98msam-6wUgACbwAD29t-AAGZW1Coe5OAdDYE",
    )
    await update.message.reply_html(reply.format(name=user.mention_html()))
