from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Text

from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message

mappings={"地域":"location",
          "人名": "person"
         }

def normalize_entity(t):
    kind = t
    if t in mappings:
        kind = mappings.get(t)
    return kind

def get_position(ps, id):
    for k,v in ps:
        if k==id:
            return v
    return None

class CabochaEntityExtractor(EntityExtractor):
    # name = "ner_hanlp"
    name="sagas.provider.cabocha_entity_extractor.CabochaEntityExtractor"

    provides = ["entities"]

    requires = ["cabocha"]

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        filters = mappings.keys()
        extracted = self.add_extractor_name(self.extract_entities(
            message.get("cabocha_doc"),
            message.get("positions"),
            filters))
        message.set("entities",
                    message.get("entities", []) + extracted,
                    add_to_output=True)

    @staticmethod
    def extract_entities(msg_tokens, positions, filters):
        entities = []
        for chunk in msg_tokens.chunks:
            for token in chunk.tokens:
                pos_set = (token.pos, token.pos1, token.pos2, token.pos3)
                for filter in filters:
                    if filter in pos_set:
                        pos=get_position(positions, token.id)
                        entities.append({
                            "entity": normalize_entity(filter),
                            "value": token.surface,
                            "start": pos["start"],
                            "confidence": None,
                            "end": pos["end"]
                        })
        return entities

