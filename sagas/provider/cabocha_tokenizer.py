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


class CabochaTokenizer(Tokenizer, Component):
    """
    Parse sentence with cabocha analyzer grpc-service
    """
    # name = "tokenizer_hanlp"
    name="sagas.provider.cabocha_tokenizer.CabochaTokenizer"

    provides = ["tokens"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None

        for example in training_data.training_examples:
            tokens, positions=self.tokenize(example.text, example.get("cabocha_doc"))
            example.set("tokens", tokens)
            example.set("positions", positions)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        tokens, positions = self.tokenize(message.text, message.get("cabocha_doc"))
        message.set("tokens", tokens)
        message.set("positions", positions)

    def tokenize(self, text, msg_chunks):
        words = []
        ids=[]
        for chunk in msg_chunks.chunks:
            for token in chunk.tokens:
                # print(token, token.pos)
                words.append(token.surface)
                ids.append(token.id)

        running_offset = 0
        tokens = []
        positions = []
        for word in words:
            word_offset = text.index(word, running_offset)
            word_len = len(word)
            running_offset = word_offset + word_len
            tokens.append(Token(word, word_offset))
            positions.append({"start":word_offset, "end":running_offset})
        return tokens, zip(ids, positions)
