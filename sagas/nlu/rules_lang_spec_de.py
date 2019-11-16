from sagas.nlu.inspectors import DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns
from sagas.nlu.lang_spec_intf import LangSpecBase, agency
from sagas.nlu.inspector_rasa import RasaInspector as intentof
import sagas.tracker_fn as tc

class Rules_de(LangSpecBase):
    # def general_rules(self):
    #     domains, meta = (self.domains, self.meta)
    #     self.collect(pats=[Patterns(domains, meta, 5, name='tech').entire(RasaInspector('tech', 0.6, True)),])

    def aux_rules(self):
        domains, meta=(self.domains, self.meta)
        rs = [Patterns(domains, meta, 2).aux(nsubj_pass=agency, obl=DateInspector('time')),
              # $ sd 'Shenzhen ist das Silicon Valley für Hardware-Firmen'
              Patterns(domains, meta, 5, name='corporation').entire(intentof('tech', 0.6, True)),
              # $ sd 'Die Nutzung der Seite ist kostenlos.' (该网站的使用是免费的。)
              Patterns(domains, meta, 5, name='website_access').aux('adj', nsubj=intentof('using', 0.6, False), cop='c_aux'),
              ]
        self.collect(pats=rs)

    def execute(self):
        if len(self.matched)>0:
            matched_info={k:len(v.results) for k,v in self.matched.items()}
            tc.emp('green', f"♯ matched id rules: {matched_info}")

