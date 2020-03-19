from typing import Text, Any, Dict, List, Union
from sagas.nlu.inspector_common import Inspector, Context


class InformInspector(Inspector):
    """
    Instances: inform('track'),

    Examples:
        >>> from sagas.nlu.nlu_startup import NluStartup
        >>> NluStartup().start()
        >>>
        >>> from sagas.nlu.parse_client_helper import build_context
        >>> from sagas.nlu.rules_header import *
        >>>
        >>> data={'lang': 'pt', "sents": 'A folha tem vinte centímetros.'}
        >>> ctx,pat=next(build_context(data, 'verb', name='_test_', engine='corenlp'))
        >>> print(ctx.engine)
        >>>
        >>> all_of=lambda *arg: all([r[1] for r in arg])
        >>> rs=pat(inform('track'), obj=kindof('unit_of_measurement', 'n'))
        >>> (rs[1], rs[0], rs[3].results)
    """
    def __init__(self, signal:Text, **kwargs):
        self.signal=signal
        self.parameters=kwargs

    def name(self):
        return "inform"

    def run(self, key, ctx:Context):
        from sagas.nlu.signals import signals
        results=signals.fire(self.name(), self.signal, key=key,
                             ctx=ctx, **self.parameters)
        for r in results:
            ctx.add_result(self.name(), provider=r['name'],
                           part_name=key, val=r['result'])
        return True

    @property
    def when_succ(self):
        return True

    def __str__(self):
        return f"ins_{self.name()}({self.signal}|{self.parameters})"


