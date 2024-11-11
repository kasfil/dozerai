import logging

from telegram import Update
from telegram import error as tele_error
from telegram.ext import ContextTypes

from config import FUND_REQ_IDLE, MAX_MSG_CHARS
from helper import scheduler


async def send_messages(
    update: Update | None,
    context: ContextTypes.DEFAULT_TYPE,
    msgs: list[str],
) -> None:
    chat_id: int
    if update and update.effective_message:
        chat_id = update.effective_message.chat_id
    elif context and context.job and context.job.chat_id:
        chat_id = context.job.chat_id
    else:
        return

    for msg in msgs:
        try:
            if update and update.message:
                await update.message.reply_markdown_v2(msg)
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                )
        except tele_error.BadRequest as e:
            if e.message == "Message is too long":
                current_idx = 0
                while current_idx < len(msg):
                    next_idx = msg.rfind("\n", current_idx, current_idx + MAX_MSG_CHARS)

                    if next_idx == -1:
                        next_idx = msg.rfind(". ", current_idx, current_idx + MAX_MSG_CHARS)

                    if next_idx == -1:
                        logging.error("can't find cut point")
                        logging.error(msg)
                        break

                    if update and update.message:
                        await update.message.reply_markdown_v2(msg[current_idx:next_idx].strip())
                    else:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=msg[current_idx:next_idx].strip(),
                        )
                    current_idx = next_idx + 1

    if not context.job_queue or FUND_REQ_IDLE <= 0:
        return

    job_name = f"fund_{chat_id}"
    current_job_queue = context.job_queue.get_jobs_by_name(job_name)

    for j in current_job_queue:
        if not j.removed:
            j.schedule_removal()

    context.job_queue.run_once(
        scheduler.fund_request,
        when=float(FUND_REQ_IDLE),
        chat_id=chat_id,
        name="fund_" + str(chat_id),
    )
