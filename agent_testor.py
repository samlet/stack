#!/usr/bin/env python

from rasa_core.interpreter import RegexInterpreter
import os
import sys
import json
# from httpretty import httpretty

from rasa_core.train import train_dialogue_model
from rasa_core.agent import Agent
from rasa_core.utils import EndpointConfig, AvailableEndpoints

def load_agent():
    p = "examples/formbot/"
    strpath=os.path.join(p, "models", "dialogue")
    endpoint = EndpointConfig("http://localhost:5055/webhook")
    endpoints = AvailableEndpoints(action=endpoint)
    loaded = Agent.load(strpath, interpreter=RegexInterpreter(), action_endpoint=endpoints.action)
    # loaded = Agent.load(strpath, interpreter=RegexInterpreter())
    responses = loaded.handle_text("/request_restaurant")
    print(responses[0])
    responses = loaded.handle_text("/chitchat")
    print(responses)

if __name__ == '__main__':
    load_agent()    
