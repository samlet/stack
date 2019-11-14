from sagas.ofbiz.connector import OfbizConnector
from sagas.ofbiz.finder import Finder
from sagas.ofbiz.util import QueryHelper
from sagas.conf.conf import cf

class Platform(object):
    def __init__(self, oc):
        self.oc=oc
        self.finder = Finder(oc)
        self.helper = QueryHelper(self.oc, self.finder)

# platform singleton
platform=Platform(oc = OfbizConnector(host=cf.conf['ofbiz_servant']))

