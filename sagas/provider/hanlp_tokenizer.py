from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Any, List, Text

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.tokenizers.tokenizer import Tokenizer, Token
from rasa.nlu.training_data import Message
from rasa.nlu.training_data import TrainingData


class HanlpTokenizer(Tokenizer, Component):
    # name = "tokenizer_hanlp"
    name="sagas.provider.hanlp_tokenizer.HanlpTokenizer"

    provides = ["tokens"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None

        for example in training_data.training_examples:
            example.set("tokens", self.tokenize(example.text, example.get("hanlp_doc")))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("tokens", self.tokenize(message.text, message.get("hanlp_doc")))

    def tokenize(self, text, msg_tokens):
        words = []
        for token in msg_tokens.entities:
            words.append(token.value)

        running_offset = 0
        tokens = []
        for word in words:
            word_offset = text.index(word, running_offset)
            word_len = len(word)
            running_offset = word_offset + word_len
            tokens.append(Token(word, word_offset))
        return tokens

