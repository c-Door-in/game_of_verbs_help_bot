import logging
from textwrap import dedent

from environs import Env
from google.cloud import dialogflow
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters


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


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    # return dedent(f'''
    #     Query text: {response.query_result.query_text}\n
    #     Detected intent: {response.query_result.intent.display_name} (confidence: {response.query_result.intent_detection_confidence})\n
    #     Fulfillment text: {response.query_result.fulfillment_text}\n
    # ''')

    return response.query_result.fulfillment_text


async def echo(update, context):
    project_id = 'instant-duality-351619'
    user_id = update.effective_user.id
    text = update.message.text
    query_text = detect_intent_texts(project_id, user_id, text, 'Russian-ru')
    await update.message.reply_text(query_text)


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
