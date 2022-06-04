import logging
from time import sleep

import telegram
from environs import Env
from google.cloud import dialogflow
from telegram import ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater


logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, context):
    user = update.effective_user
    update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def bad_command(update, context):
    logger.warning('inside bad')
    context.bot.wrong_method_name()


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


def echo(update, context):
    project_id = 'instant-duality-351619'
    user_id = update.effective_user.id
    text = update.message.text
    query_text = detect_intent_texts(project_id, user_id, text, 'Russian-ru')
    update.message.reply_text(query_text)


def error_handler(update, context):
    logger.error(msg="Исключение при обработке сообщения:", exc_info=context.error)


def main():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
    fmtdate = '%H:%M:%S'
    formater = logging.Formatter(fmtstr, fmtdate)
    ch.setFormatter(formater)
    logger.addHandler(ch)
    
    logger.warning('Start program')

    env = Env()
    env.read_env()
    tg_chat_id = env.str('TG_CHAT_ID')
    tg_admin_bot = telegram.Bot(env.str('TG_ADMIN_BOT_TOKEN'))
    tg_logs_handler = TelegramLogsHandler(tg_admin_bot, tg_chat_id)
    tg_logs_handler.setLevel(logging.WARNING)
    logger.addHandler(tg_logs_handler)

    updater = Updater(token=env.str("TGBOT_TOKEN"))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bad_command", bad_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error_handler)
    
    # tg_logs_handler = TelegramLogsHandler(tg_admin_bot, tg_chat_id)
    # tg_logs_handler.setLevel(logging.WARNING)
    # logger.addHandler(tg_logs_handler)
    logger.warning('Проверка')

    updater.start_polling()
    updater.idle()
        


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception:
            logger.exception('Ошибка в game-of-verbs-help-tg-bot. Перезапуск через 15 секунд.')
            sleep(15)
