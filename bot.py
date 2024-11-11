import logging
import sys

from telegram import LinkPreviewOptions, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, Defaults, MessageHandler, filters

from commands import ask, imgprocess, profile, rate, redeem, start, token
from commands import update as webapp_data
from config import BOT_TOKEN, DEBUG

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO if DEBUG else logging.WARNING,
)

if not DEBUG:
    logging.getLogger("telegram").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
else:
    logging.getLogger("telegram").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

default = Defaults(
    parse_mode=ParseMode.MARKDOWN_V2,
    link_preview_options=LinkPreviewOptions(show_above_text=True),
)


if __name__ == "__main__":
    if not BOT_TOKEN:
        logging.error("No token provided")
        sys.exit(1)

    application = Application.builder().token(BOT_TOKEN).defaults(default).build()
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data.web_app_data),
    )
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("ask", ask.ask))
    application.add_handler(CommandHandler("rate", rate.rate))
    application.add_handler(CommandHandler("profile", profile.profile))
    application.add_handler(CommandHandler("mytoken", token.user_token))
    application.add_handler(CommandHandler("redeem", redeem.redeem))
    application.add_handler(MessageHandler(filters.PHOTO, imgprocess.process_img))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
