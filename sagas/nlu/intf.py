from typing import Text, Any, Dict, List, Union, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json


class cla_meta_intf:
    @property
    def sents(self):
        raise NotImplementedError('Property not implemented!')

    @property
    def lang(self):
        raise NotImplementedError('Property not implemented!')

    @property
    def engine(self):
        raise NotImplementedError('Property not implemented!')

    def add_result(self, inspector: Text, provider: Text, part_name: Text,
                   val:Any, delivery_type='slot'):
        pass

@dataclass_json
@dataclass
class Entity:
    start: int
    end: int
    extractor: Text
    value: Text
    entity: Text
    confidence: float

