from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.inspectors import DateInspector as dateins
# from sagas.tool.misc import color_print
import sagas.tracker_fn as tc
from sagas.tool.package_helper import ClassFinder


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

agency=['c_pron', 'c_noun', 'c_propn']
behaviours_obl = lambda domains, meta, rs: [Patterns(domains, meta, 5).verb(behaveof(r, 'v'), obl='c_noun') for r in rs]
actions_vob = lambda domains, meta, rs: [Patterns(domains, meta, 5).verb(behaveof(r[0], 'v'), __engine='ltp', vob=kindof(r[1], 'n')) for r in rs]

class RuleSet(object):
    def __init__(self, name, rules, executor, **kwargs):
        self.name=name
        self.rules=rules
        self.executor=executor
        self.parameters=kwargs

    def __call__(self, domains, meta, ctx=None, param_sents=None):
        rule_rs = self.rules(domains, meta)
        # .. parts {'sbv': '你', 'vob': '电脑', 'wp': '？'}
        tc.info('.. parts', {k: v for k, v in rule_rs[0][3].lemmas.items()})
        if all([val[1] for val in rule_rs]):
            results = [el for r in rule_rs for el in r[3].results]
            # .. results
            # ('ins_rasa', 'vob', {'intent': 'how_many', 'confidence': 0.9721028208732605})
            if len(results)>0:
                tc.info('.. results')
                tc.info([f"{r[0]}/{r[1]}" for r in results])
                # color_print('blue', json.dumps(results, indent=2, ensure_ascii=False))
                tc.emp('blue', results)

            # 如果kwargs不为空, 则利用kwargs的规则集来检测param_sents,
            # 将得到的inspectors结果集放入对应的参数名中,
            # 与rules的结果集results一起作为参数值来调用executor.
            if len(self.parameters)>0:
                tc.emp('red', 'parameters -> %s'%', '.join(self.parameters.keys()))
                if param_sents is not None:
                    tc.emp('yellow', '; '.join(param_sents))

            # .. matched: how_many_artifact
            if ctx is not None:
                self.executor(ctx)
            else:
                self.executor(self.name)
        return rule_rs

class RuleSets(object):
    pass

# ruleset里定义的patterns不会马上执行
ruleset_stats = RuleSet('how_many_artifact',
                        rules=lambda d, m: [
                            # $ sz '你有几台笔记本电脑？'
                            Patterns(d, m, 5).verb(behaveof('have', 'v'), __engine='ltp', vob=intentof('how_many', 0.75)),
                            *actions_vob(d, m, [('have', 'device/artifact'), ]),
                        ],
                        executor=lambda arg: tc.emp('red', f'.. matched: {arg}'))

ruleset_dates = RuleSet('how_old',
                        rules=lambda domains, meta: [
                            # 匹配日期维: I was born in the spring of 1982.
                            # Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=dateins('time')),
                            # $ sd 'Die Aufnahmen begannen im November.'
                            Patterns(domains, meta, 5).verb(nsubj=agency, obl=dateins('time')),
                        ],
                        executor=lambda arg: tc.emp('red', f'.. matched: {arg}'))

class BasicRuleSets(RuleSets):
    rulesets=[ruleset_stats, ruleset_dates]

class RuleSetRunner(InspectorFixture):
    def __init__(self):
        import sagas.nlu.patterns as pat
        super().__init__()
        pat.print_not_matched = True

    def display_result_df(self, rs, presenter='jupyter'):
        df = result_df(rs)
        if presenter == 'jupyter':
            from IPython.display import display
            display(df)
        else:
            print(df)

    def procs_common(self, data, presenter='jupyter'):
        domains, meta = self.request_domains(data, presenter)
        # domains, meta=self.request_domains(data)

        rs = [Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=DateInspector('time')),
              Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=EntityInspector('GPE')),
              # Patterns(domains, meta, 2).verb(nsubj=agency, xcomp=PredicateWordInspector('color', 'n')),
              ]

        # execute patterns within the ruleset
        # rule_rs = ruleset_stats.rules(domains, meta)
        # print('.. parts', {k:v for k,v in rule_rs[0][3].lemmas.items()})
        # if all([val[1] for val in rule_rs]):
        #     results=[el for r in rule_rs for el in r[3].results]
        #     print('.. results')
        #     from sagas.tool.misc import color_print
        #     color_print('blue', results)
        #     ruleset_stats.executor(ruleset_stats.name)

        rule_rs = ruleset_stats(domains, meta)

        # display match results table
        # df = result_df(rs + rule_rs)
        # if presenter == 'jupyter':
        #     from IPython.display import display
        #     display(df)
        # else:
        #     print(df)

        self.display_result_df(rs + rule_rs)

    def test_zh(self, disable_predicts=True):
        """
        $ python -m sagas.nlu.ruleset test_zh
        $ python -m sagas.nlu.ruleset test_zh False
        :return:
        """
        text = '你有几台笔记本电脑？'
        data = {'lang': 'zh', "sents": text, 'engine': 'ltp', 'disable_predicts':disable_predicts}
        self.procs_common(data, presenter='table')

    def test_de(self):
        """
        $ python -m sagas.nlu.ruleset test_de
        :return:
        """
        text = 'Die Aufnahmen begannen im November.'
        data = {'lang': 'de', "sents": text, 'engine': 'corenlp', 'disable_predicts': False}
        domains, meta = self.request_domains(data)
        rule_rs = ruleset_dates(domains, meta)
        self.display_result_df(rule_rs)

    def check_rules(self, domains, meta):
        from termcolor import colored
        from sagas.util.reflect_util import all_subclasses

        rulesets = [rule for c in all_subclasses(RuleSets) for rule in c.rulesets]
        # print(rulesets)
        # for i, ruleset in enumerate(BasicRuleSets.rulesets):
        for i, ruleset in enumerate(rulesets):
            print(colored(f"✁ {i}. {'-' * 25}", 'cyan'))
            rule_rs = ruleset(domains, meta)
            self.display_result_df(rule_rs)

    def import_rules_pkg(self, package: object):
        # import pkgutil
        # import importlib
        # from sagas.util.reflect_util import all_subclasses
        #
        # results = {}
        # print(package.__path__)
        # for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        #     if name.startswith('rules_'):
        #         full_name = package.__name__ + "." + name
        #         results[full_name] = importlib.import_module(full_name)
        #
        # print(results.keys())
        # print(all_subclasses(RuleSets))
        executor = ClassFinder(RuleSets)
        actions = executor.register_package("sagas.aifuncs")
        for action in actions:
            print(action)

    ## issues: 用fire启动则不能列举出包中的RuleSets子类, 但在jupyter环境下是能够列举的.
    def rules_pkgs(self):
        """
        $ python -m sagas.nlu.ruleset_main
        :return:
        """
        import sagas.aifuncs
        self.import_rules_pkg(sagas.aifuncs)

    def test_all(self):
        """
        $ python -m sagas.nlu.ruleset test_all
        $ python -m sagas.nlu.ruleset_main
        :return:
        """
        import sagas.aifuncs

        text = 'Die Aufnahmen begannen im November.'
        data = {'lang': 'de', "sents": text, 'engine': 'corenlp', 'disable_predicts': False}
        domains, meta = self.request_domains(data)

        self.import_rules_pkg(sagas.aifuncs)
        self.check_rules(domains, meta)

if __name__ == '__main__':
    import fire
    fire.Fire(RuleSetRunner)

