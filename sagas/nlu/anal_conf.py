class AnalConf(object):
    def __init__(self, lang):
        from sagas.conf import resource_path
        import json_utils
        from os import path
        file = resource_path(f'analspa_{lang}.json')
        self.root = json_utils.read_json_file(file) if path.exists(file) else {}

    def setup(self, spa):
        for term_name, termls in self.root.items():
            spa.add_pats(term_name, list(termls.keys()))

