from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import (
    PredicateWordInspector as kindof,
    VerbInspector as behaveof,
    WordSpecsInspector as specsof,
    specs_no_subs, specs_trans, raw_fmt_pos,
    )
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.inspector_extractor import extract, extract_dt, extract_c, extract_for
from sagas.nlu.inspector_checker import CheckerInspector as checker
from sagas.nlu.inspector_sinkers import TagsInspector as tags, SeriesInspector as series, SlotsInspector as slots
from sagas.nlu.inspector_inferencer import InferencerInspector as infer
from sagas.nlu.inspector_clauses import (
    ClausesInspector as clauses, cla_expr,
    UnderstructureInspector as understructure,
    )

from sagas.nlu.parse_client_helper import check_interr

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

