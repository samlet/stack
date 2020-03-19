from typing import Text, Any, Dict, List, Union, Set

from sagas.nlu.inspector_common import Context
from blinker import NamedSignal, signal

track = signal('track')
evts=[track]

@track.connect
def console_track(sender, **kw):
    import datetime
    print("track from %r, data %r" % (sender, kw))
    return datetime.datetime.now()

