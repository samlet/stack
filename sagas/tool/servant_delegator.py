import requests
import logging

logger = logging.getLogger(__name__)

class Delegator(object):
    """
    >>> from sagas.tool.servant_delegator import Delegator
    >>> dele=Delegator()
    >>> dele.iwn_hypers(word="सेब", pos="noun")
    """
    def __init__(self):
        from sagas.conf.conf import cf
        self.delegates=cf.delegates

    def prepare(self, method):
        def service_method(**kwargs):
            if method in self.delegates:
                node_cf=self.delegates[method]
                logger.debug("%s, %s", node_cf, kwargs)
                response = requests.post(node_cf["url"],json=kwargs)
                if response.status_code == 200:
                    rs = response.json()
                    return rs
                else:
                    return []
            else:
                raise ValueError(f"Cannot find delegate {method}")
        return service_method

    def __getattr__(self, method):
        return self.prepare(method)

