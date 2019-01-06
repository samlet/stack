#!/usr/bin/env python
import logging
import os
import sys

import pytest

from rasa_nlu import data_router, config
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Trainer
from rasa_nlu.utils import zip_folder
from rasa_nlu import training_data

from rasa_nlu.training_data import TrainingData, Message

from sagas.provider.cabocha_tokenizer import CabochaTokenizer
from sagas.provider.cabocha_entity_extractor import CabochaEntityExtractor

# logging.basicConfig(level="DEBUG")
logging.basicConfig(level="INFO")
CONFIG_DEFAULTS_PATH = "sample_configs/config_defaults.yml"
DEFAULT_DATA_PATH = "data/examples/rasa/demo-rasa.json"
TEST_MODEL_PATH = "test_models/test_model_spacy_sklearn"

def component_builder():
    return ComponentBuilder()
def cabocha(component_builder, default_config):
    return component_builder.create_component("sagas.provider.cabocha_utils.Cabocha", default_config)

def default_config():
    return config.load(CONFIG_DEFAULTS_PATH)

cabocha=cabocha(component_builder(), default_config())

def test_cabocha_comps(text, nlp, nlp_doc):
    ext = CabochaTokenizer()
    
    example = Message(text, {
        "intent": "wish",
        "entities": [],
        "cabocha_doc": nlp_doc})

    # tokenizer
    ext.process(example, cabocha=nlp)
    for token in example.get("tokens"):
        print(token.text, token.offset)
    
    # entity extractor
    ext = CabochaEntityExtractor()
    ext.process(example, cabocha=nlp)
    print("total entities", len(example.get("entities", [])))
    for ent in example.get("entities"):
        print(ent)

if __name__ == '__main__':
    text="太郎は花子が読んでいる本を次郎に渡した"
    test_cabocha_comps(text, cabocha, cabocha.doc_for_text(text))

