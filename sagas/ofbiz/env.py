from sagas.ofbiz.runtime_context import platform

oc=platform.oc
class Env(object):
    @classmethod
    def home(cls):
        return oc.j.System.getProperty("user.dir")

