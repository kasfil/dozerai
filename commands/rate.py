from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from aibot.gemini import rate_gemini
from config import DB_PATH
from helper.async_sqlite import DB
from mdconverter import to_telemd


async def rate_imgs(context: ContextTypes.DEFAULT_TYPE) -> None:
    """rate image(s) sent by user."""
    current_job = context.job

    if not current_job or not isinstance(current_job.data, tuple):
        return

    caption, img_path, user_id = tuple(current_job.data)

    rating, comment = await rate_gemini(caption, img_path)
    response = to_telemd(f"**Rating:** {rating}\n\n" + comment)
    await context.bot.send_message(
        chat_id=current_job.chat_id,  # type: ignore
        text=response,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    database = DB(DB_PATH)
    last_row_id = await database.save_rating(user_id, img_path, caption, rating, comment)

    # last row id is sign of record is inserted, if only update the record user should not
    # getting new token
    if last_row_id and last_row_id > 0:
        await database.add_user_token(user_id, 1)


async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /rate is issued."""
    if not update.effective_message or not update.message or not update.message.text:
        return

    await update.message.reply_markdown_v2(
        text="""No image attached\\. Please send an image with /rate command\\.
additionally you can send caption with /rate command for telling us more\\.""",
    )
