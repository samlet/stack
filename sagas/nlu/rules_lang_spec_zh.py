from sagas.nlu.inspectors import DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns
from sagas.nlu.lang_spec_intf import LangSpecBase, agency
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_path import pred_all_path, pred_any_path
import sagas.tracker_fn as tc

class Rules_zh(LangSpecBase):
    def predicate_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sz '你有多少文件'
            pat(5, name='possessions_file').verb(behaveof('have', 'v'), a1=kindof('file/communication', 'n')),
            ])

    def execute(self):
        super().execute()


