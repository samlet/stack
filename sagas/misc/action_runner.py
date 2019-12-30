#!/usr/bin/env python
import json
import logging
import sys
from .utils import dump
from rasa_core.domain import Domain
from rasa_core_sdk import utils, Action, Tracker
from rasa_core_sdk.executor import CollectingDispatcher, ActionExecutor
import fire

DEFAULT_DOMAIN_PATH = "data/test_domains/default_with_slots.yml"
def default_domain():
    return Domain.load(DEFAULT_DOMAIN_PATH)

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.DEBUG, stream=sys.stdout)

## $ ./action_runner.py my_custom_action
def my_custom_action():
    from actions.procs.myactions import MyCustomAction

    executor=ActionExecutor()
    executor.register_action(MyCustomAction())
    domain=default_domain()
    req={
            'domain': domain.as_dict(),
            'next_action': 'my_custom_action',
            'sender_id': 'default',
            'tracker': {
                'latest_message': {
                    'entities': [],
                    'intent': {},
                    'text': None
                },
                'active_form': {},
                'latest_action_name': None,
                'sender_id': 'default',
                'paused': False,
                'followup_action': 'action_listen',
                'latest_event_time': None,
                'slots': {'name': None},
                'events': [],
                'latest_input_channel': None
            }
        }
    result=executor.run(req)
    dump(result)

if __name__ == '__main__':
    fire.Fire()

