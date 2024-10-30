import logging
from telegram import Update, error as tele_error
from telegram.ext import ContextTypes
from config import GROUP_PATH, MAX_MSG_CHARS
from telegram.constants import ParseMode


async def send_messages(sender: Update | ContextTypes.DEFAULT_TYPE, msgs: list[str]) -> None:
    for msg in msgs:
        try:
            if isinstance(sender, Update):
                await update.message.reply_markdown_v2(msg) # type: ignore
            else:
                await sender.bot.send_message(
                    chat_id=sender.job.chat_id,  # type: ignore
                    text=msg,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
        except tele_error.BadRequest as e:
            if e.message == "Message is too long":
                current_idx = 0
                while current_idx < len(msg):
                    next_idx = msg.rfind("\n", current_idx, current_idx +MAX_MSG_CHARS)

                    if next_idx == -1:
                        next_idx = msg.rfind(". ", current_idx, current_idx +MAX_MSG_CHARS)

                    if next_idx == -1:
                        logging.error("can't find cut point")
                        logging.error(msg)
                        break

                    if isinstance(sender, Update):
                        await update.message.reply_markdown_v2(msg[current_idx : next_idx].strip()) # type: ignore
                    else:
                        await sender.bot.send_message(
                            chat_id=sender.job.chat_id,  # type: ignore
                            text=msg[current_idx : next_idx].strip(),
                            parse_mode=ParseMode.MARKDOWN_V2,
                        )
                    current_idx = next_idx + 1
