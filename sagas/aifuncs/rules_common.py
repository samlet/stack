from sagas.nlu.ruleset import RuleSet, RuleSets, actions_vob, agency
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.tool.misc import color_print

ruleset_stats = RuleSet('how_many_artifact_c',
                        rules=lambda d, m: [
                            # $ sz '你有几台笔记本电脑？'
                            Patterns(d, m, 5).verb(behaveof('have', 'v'), __engine='ltp', vob=intentof('how_many', 0.75)),
                            *actions_vob(d, m, [('have', 'device/artifact'), ]),
                        ],
                        executor=lambda arg: color_print('red', f'.. matched: {arg}'))

ruleset_dates = RuleSet('how_old_c',
                        rules=lambda domains, meta: [
                            # 匹配日期维: I was born in the spring of 1982.
                            # Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=dateins('time')),
                            # $ sd 'Die Aufnahmen begannen im November.'
                            Patterns(domains, meta, 5).verb(nsubj=agency, obl=dateins('time')),
                        ],
                        executor=lambda arg: color_print('red', f'.. matched: {arg}'))

class CommonRuleSets(RuleSets):
    rulesets=[ruleset_stats, ruleset_dates]

