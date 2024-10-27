import logging
from uuid import uuid4

from telegram import Update
from telegram.ext import ContextTypes

from commands import ask, rate
from helper.imgsaver import imgsaver


async def process_img(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save image if it has media_group_id."""
    if (
        not update.effective_message
        or not update.effective_message.photo
        or not update.effective_user
    ):
        return

    # we need job queue, if i'ts not found in context, log error and return
    if not context.job_queue:
        logging.error("Job queue not found in context")
        return

    message = update.effective_message
    img_path = await imgsaver(message.photo[-1], message.media_group_id)

    if message.media_group_id and message.caption:
        if message.caption.startswith("/ask"):
            caption = message.caption[4:].strip()
            context.job_queue.run_once(
                ask.ask_by_imgs,
                float(5),
                data=(message.media_group_id, caption, None),
                name=str(message.media_group_id),
                chat_id=message.chat_id,
            )
        elif message.caption.startswith("/rate"):
            await message.reply_text(
                "Sorry, /rate command only works in single image mode.",
                reply_to_message_id=message.message_id,
            )

    elif message.caption:
        if message.caption.startswith("/ask"):
            caption = message.caption[4:].strip()
            context.job_queue.run_once(
                ask.ask_by_imgs,
                float(1),
                data=(None, caption, img_path),
                name=uuid4().hex,
                chat_id=message.chat_id,
            )
        elif message.caption.startswith("/rate"):
            caption = message.caption[5:].strip()
            context.job_queue.run_once(
                rate.rate_imgs,
                float(1),
                data=(caption, img_path, update.effective_user.id),
                name=uuid4().hex,
                chat_id=message.chat_id,
            )
