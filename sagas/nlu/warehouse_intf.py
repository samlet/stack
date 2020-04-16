from typing import Text, Any, Dict, List, Union, Optional, Set
from enum import Enum, unique
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from cached_property import cached_property
from sagas.util.str_converters import to_words, to_snake_case
from sagas.conf.conf import cf

@unique
class ResourceType(Enum):
    EntityModel=1
    EntityValue=2
    ServiceModel=3
    EntityAttribute=101
    ServiceAttribute=102

def words(str):
    return ''.join([' ' + i.lower() if i.isupper()
                    else i for i in str]).lstrip(' ')

class AnalResource(NodeMixin, object):
    name: str
    resource_type: ResourceType

    tags: Set[Text]={}
    description: str=''

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

    @cached_property
    def title(self):
        return to_words(to_snake_case(self.name), capfirst=True)

    @cached_property
    def words(self):
        return words(self.name)
