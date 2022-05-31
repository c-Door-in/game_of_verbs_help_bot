import requests
from environs import Env
from google.cloud import dialogflow


def get_phrases_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()
    training_phrases_url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response = requests.get(training_phrases_url)
    response.raise_for_status()
    phrases_json = response.json()

    project_id = 'instant-duality-351619'
    display_name = 'Устройство на работу'
    training_phrases_parts = phrases_json[display_name]['questions']
    message_texts = [phrases_json[display_name]['answer']]
    create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
