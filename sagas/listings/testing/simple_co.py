from typing import Text, Any, List, Optional, Union, Dict
from datetime import datetime

from sagas.listings.conf_intf import BaseConf

class SimpleConf(BaseConf):
    id: int
    prefix = 'translate English to German'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

class SimpleCo(object):
    def __init__(self, conf):
        self.conf=SimpleConf(**conf)

    def proc(self, input:Union[str, Dict]) -> Dict[Text, Any]:
        return {'input':input, 'result': self.conf}

