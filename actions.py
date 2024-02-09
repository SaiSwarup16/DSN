# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import os, requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUttered, ActionExecuted

class ChatGPT(object):

    def __init__(self, api_key):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def ask(self, question):
        body = {
            "model":self.model, 
            "messages":[{"role": "system", "content": "You are a helpful bot."},
                        {"role": "user", "content": question}]
        }
        result = requests.post(
            url=self.url,
            headers=self.headers,
            json=body,
        )

        if result.status_code == 200:
            chatgpt_response = result.json()
            return chatgpt_response['choices'][0]['message']['content']
        else:
            return "Sorry, I couldn't generate a response at the moment. Please try again later."

chatGPT = ChatGPT("")

class ActionResetProductSlot(Action):

    def name(self) -> Text:
        return "action_reset_product_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet('product_category', None),
                SlotSet('product_name', None)]

class ActionResetPreviousContraceptionSlot(Action):

    def name(self) -> Text:
        return "action_reset_previous_contraception_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet('previous_contraception_method', None),
                SlotSet('previous_contraception_satisfaction', None)]

class ActionResetDisconReqReasonSlot(Action):

    def name(self) -> Text:
        return "action_reset_discon_req_reason_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet('discon_req_reason', None)]

class ActionIntro(Action):

    def name(self) -> Text:
        return "action_intro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        start_intent = tracker.events[3]["parse_data"]["intent"]["name"]

        return [SlotSet('conv_start', True)] + [ActionExecuted("action_listen")] + [UserUttered(tracker.events[3]["text"], {
            "intent": {"name": tracker.events[3]["parse_data"]["intent"]["name"], "confidence": 1.0},
            "entities": []
        })]
        # return [SlotSet('discon_req_reason', None)]

class ActionAskGPT(Action):

    def name(self) -> Text:
        return "action_ask_gpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message["intent"]["name"]
        if(last_intent == 'nlu_fallback'):
            question = tracker.latest_message["text"]
        else:
            question = tracker.get_slot("gpt_question")
        answer = chatGPT.ask(question)
        dispatcher.utter_message(text = answer)
        return [SlotSet('gpt_question', None)]
