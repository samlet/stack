from cached_property import cached_property
from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from anytree.search import findall, findall_by_attr, find
from sagas.nlu.warehouse_intf import ResourceType, AnalResource
from sagas.ofbiz.entities import OfEntity as e, oc, all_entities
from sagas.conf.conf import cf
import pandas as pd
import logging

from sagas.ofbiz.entities import finder, MetaEntity, create_data_frame

logger = logging.getLogger(__name__)

class AnalAttribute(AnalResource):
    def __repr__(self):
        return _repr(self)

class AnalBucket(AnalResource):
    """
    >>> from sagas.nlu.warehouse import Warehouse
    >>> wh=Warehouse.create()
    >>> wh.entity('InventoryItemAndDetail').words, \
    >>>     wh.entity('InventoryItemAndDetail').title
    """
    def __repr__(self):
        return f"entity {self.name}"

    def records_df(self, limit=20, offset=0):
        from sagas.ofbiz.entities import record_list_df
        records = finder.find_list(self.name, limit, offset)
        return record_list_df(self.name, records)

    @property
    def meta_df(self):
        return create_data_frame(self.name)

    @cached_property
    def meta(self):
        """
        >>> from sagas.nlu.warehouse import warehouse as wh
        >>> (wh/'Person').meta.primary, (wh/'ProductPrice').meta.primary
        :return:
        """
        return MetaEntity(self.name)

class AnalRecordset(AnalResource):
    def __repr__(self):
        return _repr(self)

class AnalRecord(AnalResource):
    value: Any
    def __repr__(self):
        return _repr(self)

    def as_json(self):
        return oc.j.ValueHelper.entityToJson(self.value, oc.jmap())

