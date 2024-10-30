import os
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from aibot.gemini import ask_gemini
from config import GROUP_PATH
from helper.mdconverter import to_telemd
from helper.msg_sender import send_messages

base_reply = """To use /ask command, please send a message with your question\\.

For example:
/ask Is it safe to cut a tree in a rainy day?"""


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /ask is issued."""
    if not update.effective_message or not update.message or not update.message.text:
        return

    message = " ".join(context.args if isinstance(context.args, list) else [])
    if not message:
        await update.message.reply_markdown_v2(base_reply)
        return

    response = await ask_gemini(message)
    converted = to_telemd(response.text)
    await send_messages(update, [converted])


async def ask_by_imgs(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /ask is issued by image."""
    current_job = context.job

    if not current_job or not isinstance(current_job.data, tuple):
        return

    media_id, caption, img_path = tuple(current_job.data)

    if media_id and Path.exists(Path.joinpath(GROUP_PATH, str(media_id))):
        imgs = []
        for file in os.scandir(Path.joinpath(GROUP_PATH, str(media_id))):
            if file.is_file():
                imgs.append(Path.joinpath(Path(GROUP_PATH), str(media_id), file.name))

        response = await ask_gemini(caption, imgs)
        response = to_telemd(response.text)
        await send_messages(context, [response])

    elif img_path and Path.exists(img_path) and Path(img_path).is_file():
        response = await ask_gemini(caption, [img_path])
        response = to_telemd(response.text)
        await send_messages(context, [response])
