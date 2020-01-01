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

class Cabocha(Component):
    # name = "nlp_xxx"
    name="sagas.provider.cabocha_utils.Cabocha"

    provides = ["cabocha_doc", "cabocha"]

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
        "port": 50051
    }

    def __init__(self, component_config=None, nlp=None):
        # type: (Dict[Text, Any], ServiceClient) -> None

        self.nlp = nlp
        super(Cabocha, self).__init__(component_config)

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
            logger.info("Trying to connect cabocha rpc with "
                        "address '{}:{}'".format(rpc_host, rpc_port))

            client = ServiceClient(nlp_service, 'CabochaNlpProcsStub', rpc_host, int(rpc_port))
            return client
        except ValueError as e:  # pragma: no cover
            raise Exception("cabocha init error. {}".format(e))

    @classmethod
    # def create(cls, cfg):
    def create(
            cls, component_config: Dict[Text, Any], config: RasaNLUModelConfig
    ) -> "Component":
        component_conf = config.for_component(cls.name, cls.defaults)

        # cls.ensure_proper_language_model(nlp)
        client=cls.create_client(component_conf)
        return Cabocha(component_conf, client)

    def provide_context(self):
        # type: () -> Dict[Text, Any]

        return {"cabocha": self.nlp}

    def doc_for_text(self, text):
        request = nlp_messages.NlText(text=text)
        response = self.nlp.Tokenizer(request)
        return response

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None

        for example in training_data.training_examples:
            example.set("cabocha_doc", self.doc_for_text(example.text))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("cabocha_doc", self.doc_for_text(message.text))

    # @classmethod
    # def load(cls,
    #          model_dir=None,
    #          model_metadata=None,
    #          cached_component=None,
    #          **kwargs):
    #     # type: (Text, Metadata, Optional[Cabocha], **Any) -> Cabocha
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
        # return cls(component_config, cls.create_client(component_config))
        return cls(meta, cls.create_client(meta))


