from typing import Text, Any, List, Optional, Union, Dict
from datetime import datetime

from sagas.listings.co_data import CoResult, CoData
from sagas.listings.co_intf import BaseConf, BaseCo
import logging

logger = logging.getLogger(__name__)

class SimpleConf(BaseConf):
    id: int
    prefix = 'translate English to German'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

class SimpleCo(BaseCo):
    def __init__(self, conf):
        self.conf=SimpleConf(**conf)

    def preload(self):
        logger.info(".. load models here")

    def proc(self, input:Any) -> CoResult:
        return CoResult(code='ok', data=CoData(data=self.conf.json()))

