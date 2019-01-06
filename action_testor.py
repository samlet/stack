#!/usr/bin/env python
import json

import pytest
from httpretty import httpretty

from rasa_core.actions import action
from rasa_core.actions.action import (
    ActionRestart, UtterAction,
    ActionListen, RemoteAction,
    ActionExecutionRejection)
from rasa_core.domain import Domain
from rasa_core.events import Restarted, SlotSet, UserUtteranceReverted
from rasa_core.trackers import DialogueStateTracker
from rasa_core.utils import EndpointConfig

from rasa_core import train, server
from rasa_core.agent import Agent
from rasa_core.channels import CollectingOutputChannel, RestInput, channel
from rasa_core.dispatcher import Dispatcher
from rasa_core.domain import Domain
from rasa_core.interpreter import RegexInterpreter
from rasa_core.nlg import TemplatedNaturalLanguageGenerator
from rasa_core.policies.ensemble import SimplePolicyEnsemble, PolicyEnsemble
from rasa_core.policies.memoization import (
    Policy, MemoizationPolicy, AugmentedMemoizationPolicy)
from rasa_core.processor import MessageProcessor
from rasa_core.slots import Slot
from rasa_core.tracker_store import InMemoryTrackerStore
from rasa_core.trackers import DialogueStateTracker
from rasa_core.utils import zip_folder

DEFAULT_DOMAIN_PATH = "data/test_domains/default_with_slots.yml"

DEFAULT_STORIES_FILE = "data/test_stories/stories_defaultdomain.md"

END_TO_END_STORY_FILE = "data/test_evaluations/end_to_end_story.md"

MOODBOT_MODEL_PATH = "examples/moodbot/models/dialogue"

DEFAULT_ENDPOINTS_FILE = "data/test_endpoints/example_endpoints.yml"

@pytest.fixture(scope="session")
def default_domain():
    return Domain.load(DEFAULT_DOMAIN_PATH)
@pytest.fixture(scope="session")
def default_agent(default_domain):
    agent = Agent(default_domain,
                  policies=[MemoizationPolicy()],
                  interpreter=RegexInterpreter(),
                  tracker_store=InMemoryTrackerStore(default_domain))
    training_data = agent.load_data(DEFAULT_STORIES_FILE)
    agent.train(training_data)
    return agent

@pytest.fixture
def default_dispatcher_collecting(default_nlg):
    bot = CollectingOutputChannel()
    return Dispatcher("my-sender", bot, default_nlg)
@pytest.fixture
def default_nlg(default_domain):
    return TemplatedNaturalLanguageGenerator(default_domain.templates)
@pytest.fixture(scope="session")
def default_agent_path(default_agent, path):
    # path = tmpdir_factory.mktemp("agent").strpath
    default_agent.persist(path)
    return path

def disp_events(events):
    # assert events == [SlotSet("test", 4)]
    for ev in events:
        print(str(ev))
    
def test_action(default_dispatcher_collecting,
                                   default_domain, fun_name):
    tracker = DialogueStateTracker("default",
                                   default_domain.slots)

    endpoint = EndpointConfig("http://localhost:5055/webhook")
    # endpoint = EndpointConfig("http://0.0.0.0:5057/webhook")
    # endpoint = EndpointConfig("http://localhost:5055")
    remote_action = action.RemoteAction(fun_name, endpoint)

    events = remote_action.run(default_dispatcher_collecting,
                               tracker,
                               default_domain)
    disp_events(events)

    channel = default_dispatcher_collecting.output_channel
    print(channel.messages)

def run_fixture(fun_name, fun):
    domain=default_domain()
    agent=default_agent(domain)
    nlg=default_nlg(domain)
    dispatcher_collecting=default_dispatcher_collecting(nlg)
    fun(dispatcher_collecting, domain, fun_name)

if __name__ == '__main__':
    run_fixture("my_custom_action", test_action)

