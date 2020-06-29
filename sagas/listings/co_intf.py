from typing import Text, Any, Dict, List, Union, Optional
from pydantic import BaseModel
import abc

from sagas import AttrDict
from sagas.listings.co_data import CoResult


class BaseConf(BaseModel):
    type: str

class BaseCo(object):
    __metaclass__ = abc.ABCMeta
    def preload(self, **kwargs):
        pass

    @abc.abstractmethod
    def proc(self, conf:AttrDict, input:Any) -> CoResult:
        pass

