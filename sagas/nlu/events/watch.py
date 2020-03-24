from blinker import NamedSignal, signal

from sagas.nlu.events import ResultDataset, RequestMeta
from sagas.conf.conf import cf
import sagas.tracker_fn as tc
from pprint import pprint

watch = signal('watch')
# evts=[watch]

@watch.connect
def console_watch(sender, **kw):
    import datetime
    from sagas.nlu.nlu_tools import NluTools

    ds:ResultDataset=kw['dataset']
    meta:RequestMeta=kw['meta']

    print(f"****** watch {sender}")
    tc.emp('magenta', meta)

    tools = NluTools()
    if cf.is_enabled('print_tree'):
        tools.main_domains(meta.sents,
                           lang=meta.lang,
                           engine=meta.engine,
                           print_domains=False)

    return datetime.datetime.now()



