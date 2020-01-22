import yaml
import sagas.tracker_fn as tc

class RulesetsKit(object):
    def __init__(self):
        pass

    def execute(self, rules_file, test_intent=None, test_sents=None, show_graph=True):
        """
        $ python -m sagas.kit.rulesets_kit execute ./assets/test_rules.yml 'describe_object'
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object None False
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object '彼のパソコンは便利じゃない。' False
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_common_id.yml purpose

        :param rules_file:
        :param intent_name:
        :return:
        """
        from sagas.tool.dynamic_rules import DynamicRules
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

                    for k, rule in intent['rules'].items():
                        print('✁', '-' * 25, k)
                        if test_sents is None:
                            for ex in intent['examples']:
                                data = {'lang': lang, "sents": ex}
                                dr=DynamicRules()
                                result=dr.predict(data, rule, name=intent_name, graph=show_graph, operator=all)
                                resultset.append({'intent':intent_name, 'result':result})
                        else:
                            data = {'lang': lang, "sents": test_sents}
                            dr=DynamicRules()
                            result=dr.predict(data, rule, name=intent_name, graph=show_graph, operator=all)
                            tc.emp('blue', f"¤{intent_name}¤ result: {result}")
                            resultset.append({'intent': intent_name, 'result': result, 'data':dr.result_set})
            # else:
            #    print(f'no such intent {intent_name}.')

        return resultset

if __name__ == '__main__':
    import fire
    fire.Fire(RulesetsKit)
