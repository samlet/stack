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

import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service

if typing.TYPE_CHECKING:
    from nlpserv_pb2 import NlAmountList

class AmountExtractor(EntityExtractor):
    # name = "ner_amount"
    name = "sagas.provider.amount_extractor.AmountExtractor"

    provides = ["entities"]

    requires = ["hanlp"]

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        # can't use the existing doc here (spacy_doc on the message)
        # because tokens are lower cased which is bad for NER
        hanlp = kwargs.get("hanlp", None)
        request = nlp_messages.NlText(text=message.text)
        doc = hanlp.ParseAmountTerms(request)
        extracted = self.add_extractor_name(self.extract_entities(doc))
        message.set("entities",
                    message.get("entities", []) + extracted,
                    add_to_output=True)

    @staticmethod
    def extract_entities(doc):
        # type: (NlAmountList) -> List[Dict[Text, Any]]

        entities = [
            {
                "entity": "amount",
                "value": ent.numericVal,
                "start": ent.entity.start,
                "confidence": None,
                "end": ent.entity.end
            }
            for ent in doc.amount]
        return entities