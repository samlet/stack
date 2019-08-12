from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
import logging
logger = logging.getLogger('inspector')

default_projects={'de':'german', 'en':'english', 'fr':'french', 'ru':'russian', 'es':'spanish',
                  'zh':'chinese', 'ja':'japanese'}

class RasaInspector(Inspector):
    def __init__(self, intent:str, confidence:float, entire=False, contains_entity:list=None):
        self.intent = intent
        self.confidence=confidence
        self.contains_entity=contains_entity
        self.entire=entire

        self.endpoint = "http://localhost:5000"

    def name(self):
        return "ins_rasa"

    def run(self, key, ctx:Context):
        from sagas.nlu.rasa_procs import invoke_nlu

        lang = ctx.meta['lang']
        if lang not in default_projects:
            return False
        proj=default_projects[lang]

        def proc(cnt):
            succ=False
            logger.info('query with rasa-nlu: %s', cnt)
            # print(('query with rasa-nlu: %s'%cnt))
            resp = invoke_nlu(self.endpoint, proj, "current", cnt)
            if resp is not None:
                intent = resp["intent"]
                entities = resp['entities']

                ent_names = {ent['entity'] for ent in entities}
                intent_name = intent['name']
                intent_confidence = intent['confidence']
                logger.info('%s -> %f, with entities %s' % (intent_name,
                                                            intent_confidence,
                                                            ', '.join(ent_names)))
                # print(f'{self.intent}, {self.confidence}')
                if self.intent == intent_name and float(intent_confidence) > self.confidence:
                    # print('... matched intent and confidence')
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
        from sagas.tool.loggers import init_logger

        pat.print_not_matched=True
        init_logger()

    def procs_common(self, data):
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

if __name__ == '__main__':
    import fire
    fire.Fire(InspectorRunner)

