from telegram import Update
from telegram.ext import ContextTypes

from config import DB_PATH
from helper.async_sqlite import DB
from helper.mdconverter import to_telemd

format_reply = "🫨🫨🫨🫨\nOh snap, you just found our secret command. But nothing to see here. we still develop it."  # noqa: E501


async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /redeem is issued."""
    if not update.effective_user or not update.message:
        return

    db = DB(DB_PATH)

    user = update.effective_user
    token = await db.get_user_token(user.id)

    reply = format_reply.format(token=token, s="s" if token > 1 else "")
    await update.message.reply_markdown_v2(to_telemd(reply))
