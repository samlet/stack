from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

class Rules_de(LangSpecBase):
    # def general_rules(self):
    #     domains, meta = (self.domains, self.meta)
    #     self.collect(pats=[Patterns(domains, meta, 5, name='tech').entire(RasaInspector('tech', 0.6, True)),])
    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing').verb(behaveof('want', 'v'),),
            # $ sd 'Können Sie die Bilder entwickeln?'
            pat(5, name='develop_representation?').verb(behaveof('develop', 'v'),
                                                 nsubj=agency,
                                                 obj=kindof('representation', 'n'))
            ])

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)
        rs = [pat(3, ).aux(nsubj_pass=agency, obl=dateins('time')),
              # $ sd 'Shenzhen ist das Silicon Valley für Hardware-Firmen'
              pat(5, name='corporation').entire(intentof('tech', 0.6, True)),
              # $ sd 'Die Nutzung der Seite ist kostenlos.' (该网站的使用是免费的。)
              pat(5, name='website_access').aux('adj', nsubj=intentof('using', 0.6, False), cop='c_aux'),
              # $ sd 'Die Fotos sind in der Kamera.'
              pat(3, name='location').aux('aux', nsubj=agency, obl=agency),
              ]
        self.collect(pats=rs)

    def execute(self):
        if len(self.matched)>0:
            matched_info={k:len(v.results) for k,v in self.matched.items()}
            tc.emp('green', f"♯ matched id rules: {matched_info}")

