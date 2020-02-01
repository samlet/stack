from typing import Text, Any, Dict, List, Union
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

    def execute(self, rules_files:Union[Text, List[Text]],
                test_intent:Text=None, test_sents:Text=None,
                show_graph:bool=True) -> List[Dict[Text, Any]]:
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
        if isinstance(rules_files, str):
            rules_files=[rules_files]
        for rules_file in rules_files:
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
                                    dr=DynamicRules(rule_key=k)
                                    result=dr.predict(data, rule, name=intent_name, graph=show_graph, operator=any)
                                    resultset.append({'intent':intent_name,
                                                      'result':result,
                                                      'data': self.extract_result(dr)})
                            else:
                                data = {'lang': lang, "sents": test_sents}
                                dr=DynamicRules(rule_key=k)
                                # operator=any表示任何子句匹配均可
                                result=dr.predict(data, rule, name=intent_name, graph=show_graph, operator=any)
                                tc.emp('blue', f"¤{intent_name}¤ result: {result}")
                                priority=max(dr.priority_list) if len(dr.priority_list)>0 else 0
                                resultset.append({'intent': intent_name,
                                                  'result': result,
                                                  'priority': priority,
                                                  'confidence': priority*0.2,
                                                  'text': test_sents,
                                                  'data': self.extract_result(dr)})
                                cur_tests.append(result)

                        # all表示当前意图下的所有rules均满足条件才算匹配成功
                        if all(cur_tests):
                            self.intent_matched.append(intent_name)
                            cur_tests.clear()

        return resultset

    def as_rasa_format(self, rs:List[Dict[Text, Any]]) -> Dict[Text, Any]:
        ok_list = [intent for intent in rs if intent['result']]
        if len(ok_list)>0:
            rankings = sorted(ok_list, key=lambda e: e['confidence'], reverse=True)
            rank = rankings[0]
            return {
                'intent': {'confidence': rank['confidence'], 'name': rank['intent']},
                'text': rank['text'],
                'entities': rank['data'],
                'intent_ranking': [{'confidence': e['confidence'], 'name': e['intent']} for e in rankings[1:]],
            }
        return {}

if __name__ == '__main__':
    import fire
    fire.Fire(RulesetsKit)
