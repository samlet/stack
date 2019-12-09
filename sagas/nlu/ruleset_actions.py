class RulesetActions(object):
    def __init__(self):
        import glob
        import json_utils
        self.intents = []
        for f in glob.glob('/pi/stack/conf/ruleset_*.json'):
            rules = json_utils.read_json_file(f)
            for rule in rules:
                self.intents.append({rule['intent']: {'triggers': rule['action']}})

    def get_intents(self):
        """
        $ python -m sagas.nlu.ruleset_actions get_intents
        :return:
        """
        return self.intents

ruleset_actions=RulesetActions()

if __name__ == '__main__':
    import fire
    fire.Fire(RulesetActions)


