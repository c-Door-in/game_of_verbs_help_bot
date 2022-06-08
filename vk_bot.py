import logging
import random
from textwrap import dedent
from time import sleep

import telegram
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from loghandlers import TelegramLogsHandler
from detect_intent_texts import detect_intent_texts


logger = logging.getLogger(__name__)

def send_response(event, vk_api, response_text):
    vk_api.messages.send(
        user_id=event.user_id,
        message=response_text,
        random_id=random.randint(1, 1000)
    )
    logger.debug(dedent(f'''
        Новое сообщение:
        От меня для: {event.user_id}
        Текст: {response_text}'''
    ))


def main():
    logger.setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.warning('Start vk bot')

    env = Env()
    env.read_env()

    tg_admin_bot = telegram.Bot(token=env.str('TG_ADMIN_BOT_TOKEN', None))
    if tg_admin_bot:
        tg_admin_chat_id = env.str('TG_ADMIN_CHAT_ID')
        tg_logs_handler = TelegramLogsHandler(tg_admin_bot, tg_admin_chat_id)
        tg_logs_handler.setLevel(logging.WARNING)
        logger.addHandler(tg_logs_handler)

    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    vk_session = vk.VkApi(token=env.str('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response_text = detect_intent_texts(
                dialogflow_project_id,
                event.user_id,
                event.text,
                'Russian-ru',
            )
            logger.debug(dedent(f'''
                Новое сообщение:
                Для меня от: {event.user_id}
                Текст: {event.text}'''
            ))
            if response_text:
                send_response(event, vk_api, response_text)
        


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception:
            logger.exception('Ошибка в game-of-verbs-help-vk-bot. Перезапуск через 15 секунд.')
            sleep(15)