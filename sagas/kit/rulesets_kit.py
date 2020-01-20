import yaml
import sagas.tracker_fn as tc

class RulesetsKit(object):
    def __init__(self):
        pass

    def execute(self, rules_file, intent_name, test_sents=None, show_graph=True):
        """
        $ python -m sagas.kit.rulesets_kit execute ./assets/test_rules.yml 'describe_object'
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object None False
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object '彼のパソコンは便利じゃない。' False
        $ python -m sagas.kit.rulesets_kit execute ./assets/rs_common_id.yml purpose

        :param rules_file:
        :param intent_name:
        :return:
        """
        from sagas.tool.dynamic_rules import dynamic_rule
        with open(rules_file) as f:
            pkg = yaml.safe_load(f)
            intents = pkg['intents']
            lang=pkg['lang']
            if intent_name in intents:
                intent=intents[intent_name]

                for k, rule in intent['rules'].items():
                    print('✁', '-' * 25, k)
                    if test_sents is None:
                        for ex in intent['examples']:
                            data = {'lang': lang, "sents": ex}
                            dynamic_rule(data, rule, name=intent_name, graph=show_graph, operator=all)
                    else:
                        data = {'lang': lang, "sents": test_sents}
                        result=dynamic_rule(data, rule, name=intent_name, graph=show_graph, operator=all)
                        tc.emp('blue', f"result: {result}")
            else:
                print(f'no such intent {intent_name}.')

if __name__ == '__main__':
    import fire
    fire.Fire(RulesetsKit)
