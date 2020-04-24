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

from sagas.nlu.anal_data_types import ref_
from sagas.nlu.warehouse_bucket import AnalRecord
from sagas.nlu.warehouse_intf import ResourceType
from sagas.nlu.warehouse_service import AnalService
from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e, all_entities

logger = logging.getLogger(__name__)

class Warehouse(NodeMixin, object):
    name: str

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
    def all_services():
        return oc.all_service_names()

    @staticmethod
    def create() -> 'Warehouse':
        ents=[cf.get_bucket(e)(name=e, resource_type=ResourceType.EntityModel) for e in all_entities(include_view=True)]
        services = [AnalService(name=e, resource_type=ResourceType.ServiceModel) for e in Warehouse.all_services()]
        wh=Warehouse(name='_warehouse', children=[*ents, *services])
        return wh

    def entity(self, ent_name):
        return find(self, lambda node: node.name == ent_name and node.resource_type==ResourceType.EntityModel, maxlevel=2)

    def service(self, name):
        return find(self, lambda node: node.name == name and node.resource_type==ResourceType.ServiceModel, maxlevel=2)

    def __floordiv__(self, patt):
        """
        >>> from sagas.nlu.warehouse import warehouse as wh
        >>> wh//'find*'
        >>> wh//'*Person*'
        >>> [(el, el.words) for el in wh//'*Person*']
        :param patt:
        :return:
        """
        if isinstance(patt, str):
            r = Resolver('name')
            return r.glob(self, patt)
        elif isinstance(patt, ref_):
            val=self.resolve_entity(patt.val)
            return [val]
        else:
            return []

    def __truediv__(self, patt):
        rs= self.__floordiv__(patt)
        return rs[0] if rs else None

    def resolve_entity(self, gid):
        from sagas import from_global_id
        t, _ = from_global_id(gid)
        ent = self / t
        val=ent.meta.global_ref.get_record(gid)
        return AnalRecord(name=val.getEntityName(),
                          resource_type=ResourceType.EntityValue,
                          value=val)

    def get_gid(self, val):
        ent = self / val.getEntityName()
        return ent.meta.global_ref.get_gid(val)

    @property
    def qualified(self):
        return '_'

    def get(self, path):
        """
        >>> from sagas.nlu.warehouse import warehouse as wh
        >>> wh.get("/_/ent:Person")

        :param path:
        :return:
        """
        r = Resolver('qualified')
        return r.get(self, path)

    def ping(self) -> Tuple[bool, Dict[Text, Any]]:
        from sagas.ofbiz.services import OfService as s, oc, track
        ok, r = track(lambda a: s().testScv(defaultValue=5.5, message="hello world"))
        return ok, r

    @property
    def srv(self):
        from sagas.ofbiz.services import OfService as s
        return s()

    @property
    def ent(self):
        from sagas.ofbiz.entities import OfEntity as e
        return e()

    def e(self, dialect=None):
        """
        >>> from sagas.nlu.warehouse import warehouse as wh
        >>> wh.e('dict').refPerson('10000')

        :param dialect:
        :return:
        """
        from sagas.ofbiz.entities import OfEntity as e
        return e(dialect)

warehouse=Warehouse.create()

