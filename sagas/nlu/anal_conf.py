from typing import Text, Any, Dict, List, Union, Optional

DEFAULT_ENT_ID_SEP = "||"

class AnalConf(object):
    def __init__(self, lang:Text):
        from sagas.conf import resource_path
        import json_utils
        from os import path
        file = resource_path(f'analspa_{lang}.json')
        self.root = json_utils.read_json_file(file) if path.exists(file) else {}

    def setup(self, spa):
        for term_name, termls in self.root.items():
            for key, values in termls.items():
                label = "{}{}{}".format(term_name, DEFAULT_ENT_ID_SEP, key)
                spa.add_pats(label, values)

    @staticmethod
    def split_label(label):
        """Split Entity label into ent_label and ent_id if it contains ent_id_sep

        label (str): The value of label in a pattern entry

        RETURNS (tuple): ent_label, ent_id
        """
        if DEFAULT_ENT_ID_SEP in label:
            ent_label, ent_id = label.rsplit(DEFAULT_ENT_ID_SEP, 1)
        else:
            ent_label = label
            ent_id = None

        return ent_label, ent_id

conf_map={}
def anal_conf(lang):
    if lang not in conf_map:
        conf_map[lang]=AnalConf(lang)
    return conf_map[lang]

