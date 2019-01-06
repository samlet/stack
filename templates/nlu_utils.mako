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

from rasa_nlu.components import Component
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData

from client_wrapper import ServiceClient

import ${package_name}_pb2 as nlp_messages
import ${package_name}_pb2_grpc as nlp_service

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from rasa_nlu.model import Metadata

class ${class_name}(Component):
    # name = "nlp_xxx"
    name="sagas.provider.${file_name}.${class_name}"

    ## the ${component_name}_doc is protobuf object, ${component_name} is grpc client
    provides = ["${component_name}_doc", "${component_name}"]

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
        super(${class_name}, self).__init__(component_config)   

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
            logger.info("Trying to connect ${component_name} rpc with "
                        "address '{}:{}'".format(rpc_host, rpc_port))

            client = ServiceClient(nlp_service, '${service_name}Stub', rpc_host, int(rpc_port))
            return client
        except ValueError as e:  # pragma: no cover
            raise Exception("${component_name} init error. {}".format(e))

    @classmethod
    def create(cls, cfg):
        # type: (RasaNLUModelConfig) -> ${class_name}

        component_conf = cfg.for_component(cls.name, cls.defaults)

        # cls.ensure_proper_language_model(nlp)
        client=cls.create_client(component_conf)
        return ${class_name}(component_conf, client)

    def provide_context(self):
        # type: () -> Dict[Text, Any]

        return {"${component_name}": self.nlp}

    #* must be implement
    def doc_for_text(self, text):
        request = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text=text))
        response = self.nlp.EntityExtractor(request)
        return response      

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None

        for example in training_data.training_examples:
            example.set("${component_name}_doc", self.doc_for_text(example.text))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("${component_name}_doc", self.doc_for_text(message.text))

    @classmethod
    def load(cls,
             model_dir=None,
             model_metadata=None,
             cached_component=None,
             **kwargs):
        # type: (Text, Metadata, Optional[${class_name}], **Any) -> ${class_name}

        if cached_component:
            return cached_component

        component_config = model_metadata.for_component(cls.name)
        return cls(component_config, cls.create_client(component_config))


