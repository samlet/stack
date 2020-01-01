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

from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message
from py4j.java_gateway import JavaGateway, GatewayParameters
import py4j
from rasa_nlu.components import Component

if typing.TYPE_CHECKING:
    from py4j.java_gateway import JavaObject, JavaGateway

class TimeExtractor(EntityExtractor):
    """Adds entity normalization by analyzing found entities and
    transforming them into regular formats."""

    # name = "ner_xxx"
    name = "sagas.provider.time_extractor.TimeExtractor"

    provides = ["entities", "time_clean_sent"]

    defaults = {
        # dimensions can be configured to contain an array of strings
        # with the names of the dimensions to filter for
        "dimensions": None,
        "host": "localhost",
        "port": 25333
    }

    def __init__(self, component_config=None, gateway=None, bridge=None):
        # type: (Dict[Text, Any], JavaGateway, JavaObject) -> None

        super(TimeExtractor, self).__init__(component_config)
        self.gateway=gateway
        self.bridge = bridge
        if self.bridge is None:
            self.bridge = gateway.entry_point.getTimeAnalyst()
        self.DateUtil=gateway.jvm.com.time.util.DateUtil()

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["py4j"]

    @classmethod
    def create_bridge(cls, component_config):
        try:
            host = component_config.get("host")
            port= int(component_config.get("port"))
            logging.info("time-nlp gateway host/port: {} {}".format(host, port))
            gateway = JavaGateway(gateway_parameters=GatewayParameters(address=host, port=port))
            analyst = gateway.entry_point.getTimeAnalyst()
            return gateway, analyst
        except ValueError as e:  # pragma: no cover
            raise Exception("time-nlp init error. {}".format(e))

    # @classmethod
    # def create(cls, config):
    #     # type: (RasaNLUModelConfig) -> TimeExtractor
    @classmethod
    def create(
            cls, component_config: Dict[Text, Any], config: RasaNLUModelConfig
    ) -> "TimeExtractor":

        component_config = config.for_component(cls.name, cls.defaults)
        dims = component_config.get("dimensions")
        # if dims:
        gateway, analyst=cls.create_bridge(component_config)
        return TimeExtractor(component_config, gateway, analyst)

    # @classmethod
    # def cache_key(cls, model_metadata):
    #     # type: (Metadata) -> Optional[Text]
    #
    #     return None

    def f(self, object, fld):
        return py4j.java_gateway.get_field(object, fld)

    def positions(self, words, text):
        running_offset = 0
        tokens = []
        for word in words:
            # print(word)
            word_offset = text.index(word, running_offset)
            word_len = len(word)
            running_offset = word_offset + word_len
            tokens.append({"start": word_offset, "end": running_offset})
        return tokens

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        if self.bridge is None:
            logging.fatal("no time-nlp provider")
            return

        normalizer = self.bridge.getNormalizer()
        normalizer.parse(message.text)
        units = normalizer.getTimeUnit()
        entities = []

        # getting positions info
        words = []
        for unit in units:
            expr = self.f(unit, "Time_Expression")
            words.append(expr)

        clean_sent=normalizer.getTarget()
        message.set("time_clean_sent", clean_sent)
        tokens = self.positions(words, clean_sent)

        for index, ent in enumerate(units):
            entities.append({
                    "entity": "time",
                    "value": self.DateUtil.formatDateDefault(ent.getTime()),
                    "start": tokens[index]["start"],
                    "confidence": None,
                    "end": tokens[index]["end"],
                    "additional_info": str(ent.getIsAllDayTime())
                })

        extracted = self.add_extractor_name(entities)
        message.set("entities", message.get("entities", []) + extracted,
                    add_to_output=True)

    # @classmethod
    # def load(cls,
    #          model_dir=None,  # type: Text
    #          model_metadata=None,  # type: Metadata
    #          cached_component=None,  # type: Optional[TimeExtractor]
    #          **kwargs  # type: **Any
    #          ):
    #     # type: (...) -> TimeExtractor
    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional["Metadata"] = None,
            cached_component: Optional["Component"] = None,
            **kwargs: Any,
    ) -> "TimeExtractor":

        # component_config = model_metadata.for_component(cls.name)
        gateway, analyst = cls.create_bridge(meta)
        return cls(meta, gateway, analyst)

