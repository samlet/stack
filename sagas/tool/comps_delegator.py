import requests
import logging
from sagas.conf.conf import cf

logger = logging.getLogger(__name__)

class _base_executor(object):
    def __init__(self, profile, method):
        self.profile = profile
        self.method = method

    def desc(self):
        return {}

class _remote_executor(_base_executor):
    def __init__(self, profile, method):
        super().__init__(profile, method)
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


class _local_executor(_base_executor):
    def __init__(self, profile, method):
        super().__init__(profile, method)

    def __call__(self, **kwargs):
        from sagas.listings.listings_cli import listings
        return listings.proc(self.profile, self.method, kwargs)

class CompsDelegator(object):
    def __init__(self, profile, mode):
        self.profile = profile
        self.mode=mode

    def prepare(self, method):
        return _remote_executor(self.profile, method) if self.mode=='remote' \
            else _local_executor(self.profile, method)

    def __getattr__(self, method):
        return self.prepare(method)


class ProfileDelegator(object):
    """
    >>> import sagas
    >>> sagas.profs.simple.Simple(sentence='Hugging Face is a technology company')
    >>> sagas.profs.simple.Simple.desc()
    >>> sagas.profs.local_mode()  # switch to local run mode
    >>> r = sagas.profs.simple.Simple(sentence='Hugging Face is a technology company')
    """
    run_mode:str='remote'
    def __getattr__(self, method):
        return CompsDelegator(method, self.run_mode)

    def local_mode(self):
        self.run_mode='local'

    def remote_mode(self):
        self.run_mode='remote'

profs=ProfileDelegator()

