import requests
import json
from rasa_sdk import Action
from rasa_sdk.events import SlotSet


class ActionJoke(Action):
    def name(self):
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        request = requests.get('http://api.icndb.com/jokes/random').json()  # make an api call
        joke = request['value']['joke']  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionAboutDate(Action):
    def name(self):
        return "action_about_date"

    def run(self, dispatcher, tracker, domain):
        print('✁','-'*10)
        print(tracker.latest_message)
        print('✁', '-' * 10)

        dispatcher.utter_message("{}".format('all done.'))
        return [SlotSet("response", 'ok')]
