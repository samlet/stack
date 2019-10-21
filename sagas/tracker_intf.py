import abc
class TrackerIntf(abc.ABC):
    @abc.abstractmethod
    def info(self, *args, sep=' ', end='\n', file=None):
        pass
    @abc.abstractmethod
    def emphasis(self, color, *args):
        pass
    @abc.abstractmethod
    def dfs(self, *args):
        pass
    @abc.abstractmethod
    def gv(self, dot):
        pass

    @abc.abstractmethod
    def label_text(self, k, v):
        pass

    @abc.abstractmethod
    def write(self, *args):
        pass
