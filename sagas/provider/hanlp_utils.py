from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Text

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.training_data import Message
from rasa.nlu.training_data import TrainingData

from client_wrapper import ServiceClient

import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

class Hanlp(Component):
    # name = "nlp_hanlp"
    name="sagas.provider.hanlp_utils.Hanlp"

    ## the hanlp_doc is protobuf object, hanlp is grpc client
    provides = ["hanlp_doc", "hanlp"]

    defaults = {
        # name of the language model to load - if it is not set
        # we will be looking for a language model that is named
        # after the language of the model, e.g. `en`
        "model": None,

        # when retrieving word vectors, this will decide if the casing
        # of the word is relevant. E.g. `hello` and `Hello` will
        # retrieve the same vector, if set to `False`. For some
        # applications and models it makes sense to differentiate
        # between these two words, therefore setting this to `True`.
        "case_sensitive": False,
        "host": "localhost",
        "port": 10052
    }

    def __init__(self, component_config=None, nlp=None):
        # type: (Dict[Text, Any], ServiceClient) -> None

        self.nlp = nlp
        super(Hanlp, self).__init__(component_config)

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["grpc"]

    @classmethod
    def create_client(cls, component_conf):
        try:
            rpc_host = component_conf.get("host")
            rpc_port = component_conf.get("port")

            # if no model is specified, we fall back to the language string
            # if not spacy_model_name:
            logger.info("Trying to connect hanlp rpc with "
                        "address '{}:{}'".format(rpc_host, rpc_port))

            client = ServiceClient(nlp_service, 'NlpProcsStub', rpc_host, int(rpc_port))
            return client
        except ValueError as e:  # pragma: no cover
            raise Exception("hanlp init error. {}".format(e))

    # @classmethod
    # def create(cls, cfg):
    #     # type: (RasaNLUModelConfig) -> Hanlp
        # import spacy
    @classmethod
    def create(
            cls, component_config: Dict[Text, Any], config: RasaNLUModelConfig
    ) -> "Component":

        component_conf = config.for_component(cls.name, cls.defaults)

        # cls.ensure_proper_language_model(nlp)
        client=cls.create_client(component_conf)
        return Hanlp(component_conf, client)

    def provide_context(self):
        # type: () -> Dict[Text, Any]

        return {"hanlp": self.nlp}

    def doc_for_text(self, text):
        if self.component_config.get("crf_lexical"):
            request = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text=text))
            response = self.nlp.Tokenizer(request)
            return response
        else:
            request = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text=text))
            response = self.nlp.EntityExtractor(request)
            return response

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None

        for example in training_data.training_examples:
            example.set("hanlp_doc", self.doc_for_text(example.text))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("hanlp_doc", self.doc_for_text(message.text))

    # @classmethod
    # def load(cls,
    #          model_dir=None,
    #          model_metadata=None,
    #          cached_component=None,
    #          **kwargs):
    #     # type: (Text, Metadata, Optional[Hanlp], **Any) -> Hanlp
    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional["Metadata"] = None,
            cached_component: Optional["Component"] = None,
            **kwargs: Any,
    ) -> "Component":
        if cached_component:
            return cached_component

        # component_config = model_metadata.for_component(cls.name)
        return cls(meta, cls.create_client(meta))
