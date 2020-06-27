from typing import Text, Any, Dict, List, Union, Optional
from pydantic import BaseModel
import abc

from sagas.listings.co_data import CoResult


class BaseConf(BaseModel):
    type: str

class BaseCo(abc.ABC):
    def preload(self):
        pass

    @abc.abstractmethod
    def proc(self, input:Any) -> CoResult:
        pass

