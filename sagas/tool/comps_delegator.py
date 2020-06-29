import requests
import logging
from sagas.conf.conf import cf

logger = logging.getLogger(__name__)


class _executor(object):
    def __init__(self, profile, method):
        self.profile = profile
        self.method = method
        self.url = f"{cf.comps}/{self.profile}/{self.method}"

    def __call__(self, **kwargs):
        logger.debug(self.url, kwargs)
        response = requests.post(self.url, json=kwargs)
        if response.status_code == 200:
            rs = response.json()
            return rs
        else:
            return []

    def desc(self):
        return {'url': self.url}


class CompsDelegator(object):
    def __init__(self, profile):
        self.profile = profile

    def prepare(self, method):
        return _executor(self.profile, method)

    def __getattr__(self, method):
        return self.prepare(method)


class ProfileDelegator(object):
    """
    >>> import sagas
    >>> sagas.profs.simple.Simple(sentence='Hugging Face is a technology company')
    >>> sagas.profs.simple.Simple.desc()
    """
    def __getattr__(self, method):
        return CompsDelegator(method)

profs=ProfileDelegator()

