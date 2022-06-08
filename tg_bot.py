import logging
from time import sleep

import telegram
from environs import Env
from telegram import ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

from loghandlers import TelegramLogsHandler
from detect_intent_texts import detect_intent_texts


logger = logging.getLogger(__name__)

def start(update, context):
    user = update.effective_user
    update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def send_response(update, context):
    project_id = context.bot_data['dialodflow_project_id']
    user_id = update.effective_user.id
    text = update.message.text
    response_text = detect_intent_texts(project_id, user_id, text, 'Russian-ru')
    if response_text:
        update.message.reply_text(response_text)


def main():
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
    fmtdate = '%H:%M:%S'
    formater = logging.Formatter(fmtstr, fmtdate)
    ch.setFormatter(formater)
    logger.addHandler(ch)
    
    logger.warning('Start tg bot')

    env = Env()
    env.read_env()
    dialodflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    tg_admin_bot = telegram.Bot(env.str('TG_ADMIN_BOT_TOKEN', None))
    if tg_admin_bot:
        tg_admin_chat_id = env.str('TG_ADMIN_CHAT_ID')
        tg_logs_handler = TelegramLogsHandler(tg_admin_bot, tg_admin_chat_id)
        tg_logs_handler.setLevel(logging.WARNING)
        logger.addHandler(tg_logs_handler)
    while True:
        try:
            updater = Updater(token=env.str("TGBOT_TOKEN"))
            dispatcher = updater.dispatcher
            dispatcher.bot_data = {'dialodflow_project_id': dialodflow_project_id}
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_response))

            updater.start_polling()
            updater.idle()
        except Exception:
            logger.exception('Ошибка в game-of-verbs-help-tg-bot. Перезапуск через 15 секунд.')
            sleep(15)
        

if __name__ == "__main__":
    main()
