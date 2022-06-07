import argparse
import json
import pathlib

from environs import Env
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument



def create_intent(project_id, intent_name, intent_raw):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in intent_raw['questions']:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    message_texts = intent_raw['answer']
    if type(message_texts) is not list:
        message_texts = [message_texts]
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=intent_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()
    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')

    parser = argparse.ArgumentParser(description='Create intent with training phrases')
    parser.add_argument('intents_json', type=pathlib.Path, help='Path to training phrases file.')
    args = parser.parse_args()

    with open(args.intents_json, 'r', encoding="utf8") as json_file:
        intents_json = json.load(json_file)

    for intent_name, intent_raw in intents_json.items():
        try:
            create_intent(dialogflow_project_id, intent_name, intent_raw)
        except InvalidArgument as e:
            print(e)


if __name__ == '__main__':
    main()
