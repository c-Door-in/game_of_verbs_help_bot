import logging

from environs import Env
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


logger = logging.getLogger(__name__)


async def start(update, context):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update, context):
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update, context):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    env = Env()
    env.read_env()

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(env.str("TG_TOKEN")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
