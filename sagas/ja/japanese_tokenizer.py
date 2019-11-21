from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from typing import Any, List, Text

from rasa_nlu.components import Component
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.tokenizers import Tokenizer, Token
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData


class JapaneseTokenizer(Tokenizer, Component):
    """
    Parse sentence with native cabocha analyzer
    """
    name = "tokenizer_ja"

    provides = ["tokens"]

    # def train(self, training_data, config, **kwargs):
    def train(
            self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    ) -> None:
        for example in training_data.training_examples:
            example.set("tokens", self.tokenize(example.text))

    # def process(self, message, **kwargs):
    #     # type: (Message, **Any) -> None
    def process(self, message: Message, **kwargs: Any) -> None:
        message.set("tokens", self.tokenize(message.text))

    def tokenize(self, text):        
        # type: (Text) -> List[Token]

        # words=self.parse_with_cabocha(text)
        words = self.parse_with_knp(text)
        running_offset = 0
        tokens = []
        for word in words:
            word_offset = text.index(word, running_offset)
            word_len = len(word)
            running_offset = word_offset + word_len
            tokens.append(Token(word, word_offset))   
            # print(word, word_offset)
        return tokens

    def parse_with_cabocha(self, text):
        from cabocha.analyzer import CaboChaAnalyzer

        analyzer = CaboChaAnalyzer()
        tree = analyzer.parse(text)
        words = []
        for chunk in tree:
            for token in chunk:
                # print(token, token.pos)
                words.append(token.surface)
        return words

    def parse_with_knp(self, text):
        from sagas.ja.knp_helper import tokens
        return tokens(text)
