#!/usr/bin/env python
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk import Tracker, ActionExecutionRejection
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.events import SlotSet, Form
from rasa_core.domain import Domain

import warnings
import ruamel.yaml.error
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)

from actions.procs.restaurant_form import RestaurantForm

DOMAIN_PATH="examples/formbot/domain.yml"
domain=Domain.load(DOMAIN_PATH)

def test_restaurant_1():    
    form = RestaurantForm()

    ## sender_id, slots,
    #                  latest_message, events, paused, followup_action,
    #                  active_form, latest_action_name
    tracker = Tracker('default', {'requested_slot': 'cuisine'},
                      {'entities': [{'entity': 'cuisine',
                                     'value': 'some_value'},
                                    {'entity': 'some_other_slot',
                                     'value': 'some_other_value'}]},
                      [], False, None, 
                      {'name': 'restaurant_form',
                           'validate': True, 'rejected': False},
                      'action_listen')
    print("✁ req", tracker.slots, tracker.latest_message)

    dispatcher=CollectingDispatcher()
    events=form.run(dispatcher, tracker, domain)
    for ev in events:
        print(str(ev))
    print("☈", dispatcher.messages)

def test_restaurant_2():
    form = RestaurantForm()

    tracker = Tracker('default', {'requested_slot': 'cuisine'},
                      {'entities': [{'entity': 'cuisine',
                                     'value': 'chinese'},
                                    {'entity': 'some_other_slot',
                                     'value': 'some_other_value'}]},
                      [], False, None, 
                      {'name': 'restaurant_form',
                           'validate': True, 'rejected': False},
                      'action_listen')
    print("✁ req", tracker.slots, tracker.latest_message)

    dispatcher=CollectingDispatcher()
    events=form.run(dispatcher, tracker, domain)
    for ev in events:
        print(str(ev))
    print("☈", dispatcher.messages)

if __name__ == '__main__':
    print("❶")
    test_restaurant_1()
    print("❷")
    test_restaurant_2()

