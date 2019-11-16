import sagas.tracker_fn as tc

agency=['c_pron', 'c_noun', 'c_propn']

class LangSpecBase(object):
    def __init__(self, meta, domains):
        self.meta=meta
        self.domains=domains
        self.matched={}

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
        print_result(pats)
        for r in pats:
            if r[1] and r[3].name != '':
                self.matched[r[3].name] = r[3]  # r[3] is Context
