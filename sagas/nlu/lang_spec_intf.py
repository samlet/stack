from typing import Text, Dict, Any

import sagas.tracker_fn as tc

agency=['c_pron', 'c_noun', 'c_propn', 'c_det']

class LangSpecBase(object):
    def __init__(self, meta:Dict[Text,Any], domains, doc=None):
        from sagas.nlu.patterns import Patterns
        from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
        from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
        from sagas import to_obj

        self.meta=to_obj(meta)
        self.domains=domains
        self.doc=doc
        # key is pattern name, value is context(contains results)
        self.matched={}

        norm = lambda s: s.replace('/', '_').replace(' ', '_')
        self.pat = lambda p, name='': Patterns(
            self.domains, self.meta,
            p, name=name,
            doc=self.doc).opts(**self.opts())
        self.actions_obj = lambda rs: [Patterns(self.domains, self.meta, 5,
                                                name=f"act_{norm(r[0])}_{norm(r[1])}",
                                                doc=self.doc)
                                           .verb(behaveof(r[0], 'v'), obj=kindof(r[1], 'n')) for r in rs]

    @property
    def name(self):
        """Access the class's property name from an instance."""

        return type(self).name

    @staticmethod
    def prepare(meta:Dict[Text,Any]):
        pass

    def opts(self) -> Dict[Text, Any]:
        return {}

    # def general_rules(self):
    #     pass
    def verb_rules(self):
        pass
    def aux_rules(self):
        pass
    def subject_rules(self):
        pass
    def predicate_rules(self):
        pass
    def root_rules(self):
        pass

    def execute(self):
        '''
        The execute method default implementation
        :return:
        '''
        if len(self.matched)>0:
            matched_info={k:len(v.results) for k,v in self.matched.items()}
            tc.emp('blue', f"♯ matched id rules: {matched_info}")

    def collect(self, pats):
        from sagas.nlu.patterns import print_result
        print_result([p for p in pats if isinstance(p, tuple)])

        for rs in pats:
            if isinstance(rs, list):
                rows=rs
                print_result(rows)
            else:
                rows=[rs]

            for r in rows:
                # 收集成功匹配的命名rule的结果
                if r[1] and r[3].name != '':
                    self.matched[r[3].name] = r[3]  # r[3] is Context

