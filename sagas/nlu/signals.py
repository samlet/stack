from typing import Text, Any, Dict, List, Union, Set, Optional

from blinker import NamedSignal, signal

class Signals(object):
    def __init__(self):
        self.signals:List[NamedSignal]=[]

    def registry_signals(self, args:List[NamedSignal]):
        self.signals.extend(args)

    def fire(self, sender:Text, ev:Text, **kwargs) -> List[Dict[Text, Any]]:
        """
        >>> from sagas.nlu.nlu_startup import NluStartup
        >>> NluStartup().start()
        >>> from sagas.nlu.signals import signals
        >>> signals.fire('sender', 'track', key='xxx', ctx=None)
        >>> signals.fire('sender', 'tr?ck', key='xxx', ctx=None)
        >>> signals.fire('sender', 'tr*', key='xxx', ctx=None)

        :param sender:
        :param ev:
        :param key:
        :param ctx:
        :param kwargs:
        :return:
        """
        import fnmatch
        results=[]

        def proc_sig(sig):
            result = sig.send(sender, **kwargs)
            results.extend([{'name':fn.__name__, 'result':r} for fn, r in result])

        if '*' in ev or '?' in ev:
            for sig in self.signals:
                match = fnmatch.fnmatch(sig.name, ev)
                if match:
                    proc_sig(sig)
        else:
            proc_sig(signal(ev))

        return results

signals=Signals()

