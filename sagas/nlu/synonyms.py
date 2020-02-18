from typing import Text, Any, Dict, List
import yaml

class Synonyms(object):
    def __init__(self):
        # self.mappings={'id': self.load_dict('id')}
        # self.mappings={lang:self.load_dict(lang) for lang in self.availble_langs()}
        self.mappings =self.load_dataset()

    # def load_dict(self, lang):
    #     prefix = '/pi/stack/data/synonyms'
    #     file = f"{prefix}/{lang}_def.yml"
    #     with open(file, 'r') as f:
    #         return yaml.safe_load(f.read())

    def query(self, word:Text, lang:Text) -> List[Text]:
        """
        $ python -m sagas.nlu.synonyms query memulai id
        $ python -m sagas.nlu.synonyms query dorme pt
        :param word:
        :param lang:
        :return:
        """
        if lang not in self.mappings:
            return []

        syns=self.mappings[lang]
        words=syns['words']
        return words[word] if word in words else []

    def match(self, word, lang):
        # the last part of the word is lemma
        rs=self.query(word.split('/')[-1], lang)
        return rs[0] if len(rs)>0 else None

    def availble_langs(self) -> List[Text]:
        """
        $ python -m sagas.nlu.synonyms availble_langs
        :return:
        """
        return list(self.mappings.keys())

    def load_dataset(self) -> Dict[Text,Any]:
        """
        $ python -m sagas.nlu.synonyms load_dataset
        :return:
        """
        # import glob
        import ntpath
        from sagas.conf import resource_dir
        from fnmatch import fnmatch
        # prefix='/pi/stack/data/synonyms'
        # files=glob.glob(f"{prefix}/*_def.yml")
        files=resource_dir(lambda f: fnmatch(f, '*_def.yml'), 'synonyms', get_full_path=True)
        langs={}
        for file in files:
            filename=(ntpath.basename(file))
            if filename[2]=='_':
                lang=filename[:2]
                with open(file, 'r') as f:
                    langs[lang]=yaml.safe_load(f.read())

        return langs

synonyms=Synonyms()

if __name__ == '__main__':
    import fire
    fire.Fire(Synonyms)

