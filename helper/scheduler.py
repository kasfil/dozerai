from textwrap import dedent

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from helper.mdconverter import to_telemd

MSG = dedent("""*A Plea for Support: Keep Our Bot Alive!*

_Hi everyone_ 👋🏽👋🏽,

I hope this message finds you well.

I'm writing to share a bit of a challenge we're facing. As you may know, our bot has been providing valuable assistance to many of you. However, unfortunately, the developer who tirelessly created and maintains this bot hasn't received any payment since its launch.

All the costs associated with running and improving the bot, including server fees and developer time, have been borne by the developer personally. While we've been patient, the company that requested the bot has been consistently delaying the payment process.

We believe in the value this bot brings to the community and want to ensure its continued development and support. If you've found this bot helpful and would like to contribute, even a small amount can make a significant difference.

Here's how you can help:

 - Share the bot with others: Word-of-mouth is powerful!
 - Provide feedback and suggestions: Your input helps us improve the bot.
 - Consider a small donation: Every bit helps keep the bot running.

Thank you for your understanding and support. Let's work together to keep this valuable tool accessible to everyone.

Sincerely,
The Bot Team
""")  # noqa: E501


async def fund_request(context: ContextTypes.DEFAULT_TYPE) -> None:
    """send message for donation"""
    if not context.job or not context.job.chat_id:
        return

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=to_telemd(MSG),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "PayPal",
                        url="https://paypal.me/kasfildev?country.x=ID&locale.x=en_US",
                    ),
                ],
                [InlineKeyboardButton("Saweria", url="https://saweria.co/endLoopz")],
                [InlineKeyboardButton("Private channel", url="https://t.me/kasfilnews")],
            ],
        ),
    )
