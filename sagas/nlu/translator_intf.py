from typing import Text, Any, Dict, List, Union, Set
import abc

class TransTracker(object):
    def __init__(self, *obs):
        self.pronounce=[]
        # word translations as a pandas dataframe
        self.translations=None
        self.obs = list(obs)

    def add_observer(self, observer):
        if observer not in self.obs:
            self.obs.append(observer)

    def delete_observer(self, observer):
        self.obs.remove(observer)

    def notify_observers(self, meta, r=None):
        localArray = self.obs[:]
        # Updating is not required to be synchronized:
        for observer in localArray:
            observer.update(meta, r)

    def observer(self, type_of):
        return next(ob for ob in self.obs if type(ob)==type_of)


class TranslatorIntf(abc.ABC):
    @abc.abstractmethod
    def execute(self, text:Text, source:Text, target:Text,
                trans_verbose, options:Set[Text],
                tracker:TransTracker, process_result) -> Text:
        pass


def join_sentence(r):
    if len(r) == 0:
        return ''
    if r[0] is None:
        return ''

    rs = []
    for sent in r[0]:
        if sent[0] is not None:
            # print('%s ✔ %s' % (sent[0], sent[1]))
            rs.append(sent[0])
    return ' '.join(rs)

