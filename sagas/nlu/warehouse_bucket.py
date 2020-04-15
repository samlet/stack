from cached_property import cached_property
from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from anytree.search import findall, findall_by_attr, find
from sagas.util.str_converters import to_words, to_snake_case
from sagas.conf.conf import cf
import pandas as pd
import logging

from sagas.ofbiz.entities import finder, MetaEntity

logger = logging.getLogger(__name__)

def words(str):
    return ''.join([' ' + i.lower() if i.isupper()
                    else i for i in str]).lstrip(' ')

class AnalAttribute(NodeMixin, object):
    name: str

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

class AnalBucket(NodeMixin, object):
    """
    >>> from sagas.nlu.warehouse import Warehouse
    >>> wh=Warehouse.create()
    >>> wh.entity('InventoryItemAndDetail').words, \
    >>>     wh.entity('InventoryItemAndDetail').title
    """
    name: str

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

    def records_df(self, limit=20, offset=0):
        from sagas.ofbiz.entities import record_list_df
        records = finder.find_list(self.name, limit, offset)
        return record_list_df(self.name, records)

    @cached_property
    def meta(self):
        return MetaEntity(self.name)

    @cached_property
    def title(self):
        return to_words(to_snake_case(self.name), capfirst=True)

    @cached_property
    def words(self):
        return words(self.name)

class AnalRecordset(NodeMixin, object):
    name: str

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

class AnalRecord(NodeMixin, object):
    name: str

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

