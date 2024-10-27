import logging
import sys

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from commands import ask, dashboard, imgprocess, profile, rate, redeem, start, token
from config import BOT_TOKEN, DEBUG
from webapp import update as webapp_update

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


if __name__ == "__main__":
    if not BOT_TOKEN:
        logging.error("No token provided")
        sys.exit(1)

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_update.web_app_data),
    )
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("ask", ask.ask))
    application.add_handler(CommandHandler("rate", rate.rate))
    application.add_handler(CommandHandler("profile", profile.profile))
    application.add_handler(CommandHandler("mytoken", token.user_token))
    application.add_handler(CommandHandler("redeem", redeem.redeem))
    application.add_handler(CommandHandler("showui", dashboard.imgs_dashboard))
    application.add_handler(MessageHandler(filters.PHOTO, imgprocess.process_img))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
