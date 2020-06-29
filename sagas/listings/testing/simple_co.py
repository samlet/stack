from typing import Text, Any, List, Optional, Union, Dict
from datetime import datetime

from sagas import AttrDict
from sagas.listings.co_data import CoResult, CoData
from sagas.listings.co_intf import BaseConf, BaseCo
import logging

logger = logging.getLogger(__name__)

class SimpleCo(BaseCo):
    def preload(self, **kwargs):
        logger.info(".. load models here")

    def proc(self, conf:AttrDict, input:Any) -> CoResult:
        return CoResult(code='ok', data=CoData(data=conf))

