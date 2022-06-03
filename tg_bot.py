import logging
from textwrap import dedent
from time import sleep

import telegram
from environs import Env
from google.cloud import dialogflow
from telegram import ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters


logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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

    tg_admin_chat_id = env.str('TG_ADMIN_CHAT_ID')
    tg_admin_bot = telegram.Bot(token=env.str('TG_ADMIN_BOT_TOKEN'))
    tg_logs_handler = TelegramLogsHandler(tg_admin_bot, tg_admin_chat_id)
    tg_logs_handler.setLevel(logging.WARNING)
    logger.addHandler(tg_logs_handler)

    while True:
        try:
            application = ApplicationBuilder().token(env.str("TG_TOKEN")).build()
            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
            application.run_polling()
        except Exception:
            logger.exception('Ошибка в game-of-verbs-help-tg-bot. Перезапуск через 15 секунд.')
            sleep(15)


if __name__ == "__main__":
    main()
