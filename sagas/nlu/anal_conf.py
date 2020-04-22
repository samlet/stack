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

    # def get_term_props(self, term_name, ):


conf_map={}
def anal_conf(lang):
    if lang not in conf_map:
        conf_map[lang]=AnalConf(lang)
    return conf_map[lang]
