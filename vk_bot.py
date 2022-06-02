import logging
import random
from textwrap import dedent

import vk_api as vk
from environs import Env
from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__name__)


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


def echo(event, vk_api, response_text):
    vk_api.messages.send(
        user_id=event.user_id,
        message=response_text,
        random_id=random.randint(1,1000)
    )
    logger.debug(dedent(f'''
        Новое сообщение:
        От меня для: {event.user_id}
        Текст: {response_text}'''
    ))


def main() -> None:
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    env = Env()
    env.read_env()

    dialogflow_project_id = 'instant-duality-351619'

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
            print('Новое сообщение:')
            print('Для меня от: ', event.user_id)
            print('Текст:', event.text)
            echo(event, vk_api, response_text)


if __name__ == "__main__":
    main()