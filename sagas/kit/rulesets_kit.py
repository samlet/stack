import yaml
import sagas.tracker_fn as tc
from sagas.tool.dynamic_rules import DynamicRules

class RulesetsKit(object):
    def __init__(self, extractor=None):
        import os
        self.extractor = extractor or os.getenv('extractor') or 'default'
        print(f".. with extractor {self.extractor}")
        self.intent_matched = []

    def extract_result(self, dr:DynamicRules):
        return dr.rasa_ents if self.extractor=='rasa' else dr.result_set

    def execute(self, rules_file, test_intent=None, test_sents=None, show_graph=True):
        """
        $ python -m sagas.kit.rulesets_kit execute ./assets/test_rules.yml 'describe_object'
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object None False
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object '彼のパソコンは便利じゃない。' False
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_common_id.yml purpose
        $ extractor=rasa python -m sagas.kit.rulesets_kit execute ./assets/rs_common_id.yml purpose

        :param rules_file:
        :param intent_name:
        :return:
        """
        resultset=[]
        with open(rules_file) as f:
            pkg = yaml.safe_load(f)
            intents = pkg['intents']
            lang=pkg['lang']
            if test_intent is None:
                intent_candidates=intents.keys()
            else:
                intent_candidates=[test_intent]

            for intent_name in intent_candidates:
                if intent_name in intents:
                    intent=intents[intent_name]

                    cur_tests = []
                    for k, rule in intent['rules'].items():

                        print('✁', '-' * 25, k)
                        if test_sents is None:
                            for ex in intent['examples']:
                                data = {'lang': lang, "sents": ex}
                                dr=DynamicRules()
                                result=dr.predict(data, rule, name=intent_name, graph=show_graph, operator=any)
                                resultset.append({'intent':intent_name,
                                                  'result':result,
                                                  'data': self.extract_result(dr)})
                        else:
                            data = {'lang': lang, "sents": test_sents}
                            dr=DynamicRules()
                            # operator=any表示任何子句匹配均可
                            result=dr.predict(data, rule, name=intent_name, graph=show_graph, operator=any)
                            tc.emp('blue', f"¤{intent_name}¤ result: {result}")
                            resultset.append({'intent': intent_name,
                                              'result': result,
                                              'priority': max(dr.priority_list),
                                              'data': self.extract_result(dr)})
                            cur_tests.append(result)

                    # all表示当前意图下的所有rules均满足条件才算匹配成功
                    if all(cur_tests):
                        self.intent_matched.append(intent_name)
                        cur_tests.clear()

            # else:
            #    print(f'no such intent {intent_name}.')

        return resultset


if __name__ == '__main__':
    import fire
    fire.Fire(RulesetsKit)
