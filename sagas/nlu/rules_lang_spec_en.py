from sagas.nlu.inspectors import DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns
from sagas.nlu.lang_spec_intf import LangSpecBase, agency
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.inspector_path import pred_all_path, pred_any_path
import sagas.tracker_fn as tc

class Rules_en(LangSpecBase):
    def verb_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to play music.'
            pat(5, name='behave_media').verb(pred_any_path('xcomp/obj','sound/perception', 'n')),
            ])

    def execute(self):
        if len(self.matched)>0:
            matched_info={k:len(v.results) for k,v in self.matched.items()}
            tc.emp('green', f"♯ matched id rules: {matched_info}")

