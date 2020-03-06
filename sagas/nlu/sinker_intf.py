import abc
from typing import Text, Any, Dict, List, Union

class SinkerStoreIntf(abc.ABC):
    @abc.abstractmethod
    def store(self, bucket: Text, values: Dict[Text, Any], user=None):
        pass

    @abc.abstractmethod
    def get_bucket(self, bucket: Text, user=None):
        pass

