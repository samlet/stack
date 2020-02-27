from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import (
    PredicateWordInspector as kindof,
    VerbInspector as behaveof,
    WordSpecsInspector as specsof,
    )
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.inspector_extractor import extract, extract_dt, extract_c, extract_for
from sagas.nlu.inspector_checker import CheckerInspector as checker

from sagas.nlu.patterns import Patterns

from sagas.tool.misc import color_print

from sagas.nlu.aiobj_base import BaseMeta, Keeper
from sagas.nlu.ruleset import RuleSet, actions_vob, behaviours_obl

from sagas.nlu.lang_spec_intf import LangSpecBase, agency

# pred-exprs, free-exprs
from sagas.nlu.inspector_path import pred_all_path, pred_any_path, any_path
from sagas.nlu.inspector_free import comps, predict_aux, predict_subj, predict_verb
from sagas.nlu.rules_fn import anal, predicate_fn
from sagas.nlu.operators import ud

# match-exprs
from sagas.nlu.inspectors import (
    MatchInspector as matchins,
    interr_root, interr,
    CustInspector as cust)

# registry
# from sagas.nlu.inspector_registry import ci

# combine functors
from sagas.nlu.chained_patterns import chained, verb, subj

## Only includes in jupyter or test-files

