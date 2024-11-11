from telegram import Update
from telegram.ext import ContextTypes

from config import DB_PATH
from helper.async_sqlite import DB
from helper.mdconverter import to_telemd
from helper.msg_sender import send_messages

# ruff: noqa: E501
appreciation = {
    "0": "🍃 It looks like you haven’t contributed to the bot yet, but that’s okay!\nWe’re excited to have you on board! Every journey starts with a single step, and we’re looking forward to your first contribution. Let’s make safety a priority together!",
    "5": "🌱 You’ve made a small start with your contributions!\nThank you for taking your first steps toward improving health, safety, and the environment! Your input, no matter how small, is valued and helps make a difference. Keep going!",
    "10": "🌿 You’re contributing to making our community safer!\nWe appreciate your growing involvement in improving safety! Every contribution helps build a stronger, healthier environment. Your effort does not go unnoticed. Keep up the great work!",
    "20": "🌾 You’ve shared a few insights here and there, contributing to a safer workplace!\nYour efforts are appreciated! Whether it’s a quick report or an important safety recommendation, your contributions help build a culture of care and awareness. Thank you for being part of the solution!",
    "30": "🌷 You’re a regular contributor and consistently help improve safety practices!\nYour consistent contributions make a lasting impact! Thanks to you, we’re creating a safer and more sustainable environment. Your dedication to safety sets a great example for others to follow!",
    "50": "🌼 You’re an active participant in enhancing HSE standards, with valuable contributions.\nThank you for your dedication and active participation! Your contributions are making a tangible difference. You’re helping to lead the way toward a safer, healthier future for everyone. Keep it up!",
    "100": "🌳 You’ve made significant contributions, helping shape safety protocols and guidelines!\nYour commitment to improving safety is outstanding! You’re not just contributing; you’re helping drive change. Your input has a real-world impact, and we’re incredibly grateful for your passion and dedication!",
    "_": "🪺 You’re a top contributor, consistently enhancing safety and leading by example.\nYou’re a true safety champion! Your remarkable contributions have made you an integral part of this community. Thanks to you, we’re setting new standards in health, safety, and environmental care. You inspire others to join this important cause. Thank you for being a leader!",
}
# ruff: qa: #501

format_reply = """👷 Here is your profile summary:

Username: {username}

Image rated: {image_rated_count}
Average rating: {average_rating}

Reward token: {token}

{message}
"""


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /profile is issued."""
    if not update.effective_user or not update.message:
        return

    db = DB(DB_PATH)

    image_rated_count, average_rating = await db.get_user_profile(update.effective_user.id)

    user = update.effective_user
    token = await db.get_user_token(user.id)

    # determine appreciation message based on image_rated_count in appreciation dict
    appreciation_message = appreciation["_"]
    for k, v in sorted((int(k), v) for k, v in appreciation.items() if k != "_"):
        if image_rated_count <= k:
            appreciation_message = v
            break

    reply = format_reply.format(
        username=update.effective_user.mention_markdown_v2(),
        token=token,
        image_rated_count=image_rated_count,
        average_rating=f"{average_rating:.2f}",
        message=appreciation_message,
    )

    await send_messages(update, context, [to_telemd(reply)])
