import yaml

class RulesetsKit(object):
    def execute(self, rules_file, intent_name):
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
            if intent_name in intents:
                for k, rule in intents[intent_name]['rules'].items():
                    print('✁', '-' * 25, k)
                    data = {'lang': 'id', "sents": 'Gajah adalah hewan yang dilindungi.'}
                    dynamic_rule(data, rule)
            else:
                print(f'no such intent {intent_name}')

if __name__ == '__main__':
    import fire
    fire.Fire(RulesetsKit)
