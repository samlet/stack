from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
import requests

def result_df(rs):
    from sagas.conf.conf import cf
    import sagas

    # print_not_matched=cf.is_enabled('print_not_matched')
    print_not_matched=True
    recs=[]
    for r in rs:
        if not print_not_matched and not r[1]:
            pass
        else:
            recs.append(('✔' if r[1] else '✖', r[0]))
    return sagas.to_df(recs, ['match', 'options'])

class RuleSet(object):
    def __init__(self, name, rules, executor):
        self.name=name
        self.rules=rules
        self.executor=executor


class RuleSetRunner(InspectorFixture):
    def __init__(self):
        import sagas.nlu.patterns as pat
        pat.print_not_matched = True

    def procs_common(self, data, presenter='jupyter'):
        domains, meta = self.request_domains(data, presenter)
        # domains, meta=self.request_domains(data)
        agency = ['c_pron', 'c_noun']
        behaviours_obl = lambda rs: [Patterns(domains, meta, 5).verb(behaveof(r, 'v'), obl='c_noun') for r in rs]
        actions_vob = lambda rs: [
            Patterns(domains, meta, 5).verb(behaveof(r[0], 'v'), __engine='ltp', vob=kindof(r[1], 'n')) for r in rs]
        rs = [Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=DateInspector('time')),
              Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=EntityInspector('GPE')),
              # Patterns(domains, meta, 2).verb(nsubj=agency, xcomp=PredicateWordInspector('color', 'n')),
              ]

        # ruleset里定义的patterns不会马上执行
        ruleset_stats = RuleSet('how_many_artifact',
                                rules=lambda d, m: [
                                    # $ sz '你有几台笔记本电脑？'
                                    Patterns(domains, meta, 5).verb(behaveof('have', 'v'), __engine='ltp',
                                                                    vob=intentof('how_many', 0.75)),
                                    *actions_vob([('have', 'device/artifact'), ]),
                                ],
                                executor=lambda arg: print(f'matched: {arg}'))

        # execute patterns within the ruleset
        rule_rs = ruleset_stats.rules(domains, meta)
        if all([val[1] for val in rule_rs]):
            ruleset_stats.executor(ruleset_stats.name)

        df = result_df(rs + rule_rs)
        if presenter == 'jupyter':
            from IPython.display import display
            display(df)
        else:
            print(df)

    def test_zh(self, disable_predicts=True):
        """
        $ python -m sagas.nlu.ruleset test_zh
        $ python -m sagas.nlu.ruleset test_zh False
        :return:
        """
        text = '你有几台笔记本电脑？'
        data = {'lang': 'zh', "sents": text, 'engine': 'ltp', 'disable_predicts':disable_predicts}
        self.procs_common(data, presenter='table')

if __name__ == '__main__':
    import fire
    fire.Fire(RuleSetRunner)

