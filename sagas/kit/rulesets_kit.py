import yaml

class RulesetsKit(object):
    def execute(self, rules_file, intent_name, show_graph=True):
        """
        $ python -m sagas.kit.rulesets_kit execute ./assets/test_rules.yml 'describe_object'
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
                    for ex in intent['examples']:
                        data = {'lang': lang, "sents": ex}
                        dynamic_rule(data, rule, name=intent_name, graph=show_graph)
            else:
                print(f'no such intent {intent_name}.')

if __name__ == '__main__':
    import fire
    fire.Fire(RulesetsKit)
