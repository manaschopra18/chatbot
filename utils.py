import json
import os
from pymongo import MongoClient
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mybot-client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "mybot-ijxulx"

dict_news={'topic':"",'language':"",'location':""}

from gnewsclient import gnewsclient

client = gnewsclient.NewsClient(max_results=3)

def get_news(parameters):
    print("__________________________________________________________________________________________________")
    print("PARAMETERSSS = ",parameters)
    print("__________________________________________________________________________________________________")
    client.topic = parameters.get('news_type')
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    global dict_news
    dict_news={'topic':client.topic,'language':client.language,'location':client.location}
    
    return client.get_news()

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    
    if response.intent.display_name == 'get_news':
        news = get_news(dict(response.parameters))
        news_str = 'Here is your news:'
        for row in news:
            news_str += "\n\n{}\n\n{}\n\n".format(row['title'],row['link'])
        return news_str

    elif response.intent.display_name == 'jokes.get':
        return response.fulfillment_text

    elif response.intent.display_name == 'mediafile':
        return "picture10"

    else:
        return response.fulfillment_text