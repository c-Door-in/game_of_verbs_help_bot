import logging
from textwrap import dedent

from environs import Env
from google.cloud import dialogflow
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters


logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    logger.info(f"Session path: {session}")
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


async def echo(update, context):
    project_id = 'instant-duality-351619'
    user_id = update.effective_user.id
    text = update.message.text
    query_text = detect_intent_texts(project_id, user_id, text, 'Russian-ru')
    await update.message.reply_text(query_text)


def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.setLevel(logging.INFO)

    env = Env()
    env.read_env()

    application = ApplicationBuilder().token(env.str("TG_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()
