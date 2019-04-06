import json
import utils
from rasa_core.domain import Domain
from rasa_core.trackers import DialogueStateTracker, EventVerbosity
from rasa_core.events import (
    UserUttered, ActionExecuted, Restarted, ActionReverted,
    UserUtteranceReverted)
from rasa_core.actions.action import ACTION_LISTEN_NAME
from rasa_core.interpreter import RasaNLUHttpInterpreter
from rasa_core.utils import EndpointConfig, AvailableEndpoints
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.executor import ActionExecutor
from rasa_core.events import deserialise_events
import logging

# DEFAULT_DOMAIN_PATH = "data/test_domains/default_with_slots.yml"
# DEFAULT_DOMAIN_PATH = 'agents/prototypes/concertbot/domain.yml'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# def default_domain():
#     return Domain.load(DEFAULT_DOMAIN_PATH)
#
# domain=default_domain()

class ActionRunner(object):
    def __init__(self, domain_path='agents/prototypes/concertbot/domain.yml'):
        self.executor = ActionExecutor()
        action_package_name = 'actions.procs'
        self.executor.register_package(action_package_name)
        endpoint = EndpointConfig("http://localhost:5000")
        self.interpreter = RasaNLUHttpInterpreter(model_name="nlu",
                                             project_name='chinese',
                                             endpoint=endpoint)
        self.domain=Domain.load(domain_path)

    def create_api_response(self, events, messages):
        return {
            "events": events if events else [],
            "responses": messages
        }

    def prepare(self, text):
        tracker = DialogueStateTracker("default", self.domain.slots)
        parse_data = self.interpreter.parse(text)
        # print(parse_data)
        tracker.update(UserUttered(text, parse_data["intent"],
                                   parse_data["entities"], parse_data))
        # store all entities as slots
        for e in self.domain.slots_for_entities(parse_data["entities"]):
            tracker.update(e)

        print("Logged UserUtterance - "
              "tracker now has {} events".format(len(tracker.events)))
        # print(tracker.latest_message)
        return tracker

    def execute(self, action_name, text, get_tracker=False):
        """
        $ python -m sagas.bots.action_runner execute action_about_date '找音乐会'
        $ python -m sagas.bots.action_runner execute action_about_date '找音乐会' True
        $ python -m sagas.bots.action_runner execute action_joke '找音乐会'
        :param action_name:
        :param text:
        :return:
        """
        # tracker = DialogueStateTracker("default", domain.slots)
        tracker=self.prepare(text)

        dispatcher = CollectingDispatcher()
        action = self.executor.actions.get(action_name)
        events = action(dispatcher, tracker, self.domain)
        resp= self.create_api_response(events, dispatcher.messages)
        if get_tracker:
            evs = deserialise_events(events)
            for ev in evs:
                tracker.update(ev)
            return resp, tracker
        else:
            return resp

if __name__ == '__main__':
    import fire
    fire.Fire(ActionRunner)
