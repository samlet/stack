from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.patterns import Patterns

from sagas.tool.misc import color_print

from sagas.nlu.aiobj_base import BaseMeta, Keeper
from sagas.nlu.ruleset import RuleSet, actions_vob, behaviours_obl

## Only includes in jupyter or test-files
