import argparse
import requests
from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

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
    parser = argparse.ArgumentParser(description='Create intent with training phrases')
    parser.add_argument('training_phrases_url', type=str, help='URL path to training phrases file.')
    parser.add_argument('display_name', type=str, help='Intent name')
    args = parser.parse_args()
    response = requests.get(args.training_phrases_url)
    response.raise_for_status()
    phrases_json = response.json()

    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    display_name = args.display_name
    training_phrases_parts = phrases_json[display_name]['questions']
    message_texts = [phrases_json[display_name]['answer']]
    create_intent(dialogflow_project_id, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
