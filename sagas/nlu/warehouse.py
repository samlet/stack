from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set

from anytree import Resolver
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from anytree.search import findall, findall_by_attr, find

from sagas.conf.conf import cf
import pandas as pd
import logging

from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e, all_entities

logger = logging.getLogger(__name__)

class Warehouse(NodeMixin, object):

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

    @staticmethod
    def all_entities():
        return all_entities(include_view=True)

    @staticmethod
    def create() -> 'Warehouse':
        from sagas.nlu.warehouse_bucket import AnalBucket
        ents=[AnalBucket(name=e) for e in all_entities(include_view=True)]
        wh=Warehouse(name='_warehouse', children=ents)
        return wh

    def entity(self, ent_name):
        return find(self, lambda node: node.name == ent_name, maxlevel=2)

    def __floordiv__(self, patt):
        r = Resolver('name')
        return r.glob(self, patt)

