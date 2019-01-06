from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import logging
from inspect import getmembers

import typing
from typing import Any, Dict
from typing import List
from typing import Optional
from typing import Text

from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.extractors import EntityExtractor
from rasa_nlu.model import Metadata
from rasa_nlu.training_data import Message
from py4j.java_gateway import JavaGateway, GatewayParameters
import py4j

if typing.TYPE_CHECKING:
    from py4j.java_gateway import JavaObject, JavaGateway

class ${class_name}(EntityExtractor):
    """Adds entity normalization by analyzing found entities and
    transforming them into regular formats."""

    # name = "ner_xxx"
    name = "sagas.provider.${file_name}.${class_name}"

    provides = ["entities"]

    defaults = {        
        # dimensions can be configured to contain an array of strings
        # with the names of the dimensions to filter for
        "dimensions": None,
        "host": "localhost",
        "port": 25333
    }

    def __init__(self, component_config=None, gateway=None, bridge=None):
        # type: (Dict[Text, Any], JavaGateway, JavaObject) -> None

        super(${class_name}, self).__init__(component_config)
        self.gateway=gateway
        self.bridge = bridge
        if self.bridge is None:
            self.bridge = gateway.entry_point.get${component_name}()
        # self.DateUtil=gateway.jvm.com.time.util.DateUtil()

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["py4j"]

    @classmethod
    def create_bridge(cls, component_config):
        try:
            host = component_config.get("host")
            port= int(component_config.get("port"))
            logging.info("${class_name} gateway host/port: {} {}".format(host, port))
            gateway = JavaGateway(gateway_parameters=GatewayParameters(address=host, port=port))
            c = gateway.entry_point.get${component_name}()
            return gateway, c
        except ValueError as e:  # pragma: no cover
            raise Exception("${component_name} init error. {}".format(e))

    @classmethod
    def create(cls, config):
        # type: (RasaNLUModelConfig) -> ${class_name}

        component_config = config.for_component(cls.name, cls.defaults)
        dims = component_config.get("dimensions")
        # if dims:
        gateway, c=cls.create_bridge(component_config)
        return ${class_name}(component_config, gateway, c)

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Optional[Text]

        return None

    def f(self, object, fld):
        return py4j.java_gateway.get_field(object, fld)

    ##@ must be implement
    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        if self.bridge is None:
            logging.fatal("no ${component_name} provider")
            return

        entities = []
        # .......

        extracted = self.add_extractor_name(entities)
        message.set("entities", message.get("entities", []) + extracted,
                    add_to_output=True)

    @classmethod
    def load(cls,
             model_dir=None,  # type: Text
             model_metadata=None,  # type: Metadata
             cached_component=None,  # type: Optional[${class_name}]
             **kwargs  # type: **Any
             ):
        # type: (...) -> ${class_name}

        component_config = model_metadata.for_component(cls.name)
        gateway, c = cls.create_bridge(component_config)
        return cls(component_config, gateway, c)

