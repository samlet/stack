from typing import Text, Dict, Any

from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
from sagas.conf.conf import cf
import logging
logger = logging.getLogger('inspector')

# default_projects={'de':'german', 'en':'english', 'fr':'french',
#                   'ru':'russian', 'es':'spanish',
#                   'zh':'chinese', 'ja':'japanese'}
default_projects={'de', 'en', 'fr', 'ru', 'es', 'zh', 'ja'}

class RasaInspector(Inspector):
    """
    >>> from sagas.nlu.rules_header import *
    >>> # $ sd 'Shenzhen ist das Silicon Valley für Hardware-Firmen'
    >>> Patterns(domains, meta, 5).entire(intentof('tech', 0.6, True)),
    >>> # $ sd 'Die Nutzung der Seite ist kostenlos.'
    >>> Patterns(domains, meta, 5).aux('adj', nsubj=intentof('using', 0.6, False), cop='c_aux'),
    """
    def __init__(self, intent:str, confidence:float, entire=False, contains_entity:list=None):
        self.intent = intent
        self.confidence=confidence
        self.contains_entity=contains_entity
        self.entire=entire

        # self.endpoint = "http://localhost:5000"
        self.endpoint=cf.ensure('nlu_multilang_servant')
        self._result=None

    def name(self):
        return "ins_rasa"

    @property
    def result(self):
        return self._result

    def run(self, key, ctx:Context):
        from sagas.nlu.rasa_procs import invoke_nlu

        lang = ctx.meta['lang']
        if lang not in default_projects:
            return False
        # proj=default_projects[lang]
        proj=lang

        def proc(cnt:Text) -> bool:
            succ=False
            logger.debug('query with rasa-nlu: %s', cnt)
            # print(('query with rasa-nlu: %s'%cnt))
            resp = invoke_nlu(self.endpoint, proj, "current", cnt)
            if resp is not None:
                intent = resp["intent"]
                entities = resp['entities']

                ent_names = {ent['entity'] for ent in entities}
                intent_name = intent['name']
                intent_confidence = float(intent['confidence'])
                self._result=intent_confidence
                logger.info('%s(%s) -> %f, with entities %s' % (cnt, intent_name,
                                                            intent_confidence,
                                                            ', '.join(ent_names)))
                # print(f'{self.intent}, {self.confidence}')
                if self.intent == intent_name and intent_confidence > self.confidence:
                    # print('... matched intent and confidence')
                    ctx.add_result(self.name(), 'default', key,
                                   {'intent':intent_name,
                                    'confidence':intent_confidence})
                    if self.contains_entity is None:
                        succ = True
                    elif self.contains_entity is not None and ent_names.issubset(self.contains_entity):
                        succ = True
            return succ

        if self.entire:
            # print('proc -> %s'%key)
            return proc(key)
        else:
            for cnt in ctx.stem_pieces(key):
                result=proc(cnt)
                if result:
                    return True

        return False

    def __str__(self):
        return f'{self.name()} for ({self.intent})'

class InspectorRunner(InspectorFixture):
    def __init__(self):
        import sagas.nlu.patterns as pat

        super().__init__()
        pat.print_not_matched=True

    def procs_common(self, data:Dict[Text, Any]):
        domains, meta=self.request_domains(data)
        agency = ['c_pron', 'c_noun']
        intentof=RasaInspector
        rs = [Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=DateInspector('time')),
              Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=EntityInspector('GPE')),
              Patterns(domains, meta, 5).entire(RasaInspector('tech', 0.6, True)),
              Patterns(domains, meta, 5).verb(nsubj=agency, obl=intentof('context_indicator', 0.6, False)),
              Patterns(domains, meta, 5).verb(nsubj=intentof('using', 0.6, False), cop='c_aux'),
              ]
        print_result(rs)

    def test_1(self):
        """
        $ python -m sagas.nlu.inspector_rasa test_1
        :return:
        """
        texts = ['Shenzhen ist das Silicon Valley für Hardware-Firmen',
                 'Ich stimme dir in diesem Punkt nicht zu.',
                 'Die Nutzung der Seite ist kostenlos.',
                 ]
        for text in texts:
            data = {'lang': 'de', "sents": text}
            self.procs_common(data)
            print('✁', '-'*30)

"""
+ Some fixtures
    $ ses 'Yo no conduje a la escuela por la lluvia.'
    $ se 'I did not drive to school because of the rain.'
"""

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(InspectorRunner)

