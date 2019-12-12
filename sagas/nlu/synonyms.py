import yaml

class Synonyms(object):
    def __init__(self):
        # self.mappings={'id': self.load_dict('id')}
        self.mappings={lang:self.load_dict(lang) for lang in self.availble_langs()}

    def load_dict(self, lang):
        prefix = '/pi/stack/data/synonyms'
        file = f"{prefix}/{lang}_def.yml"
        with open(file, 'r') as f:
            return yaml.safe_load(f.read())

    def query(self, word, lang):
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
        verbs=syns['verbs']
        return verbs[word] if word in verbs else []

    def match(self, word, lang):
        # the last part of the word is lemma
        rs=self.query(word.split('/')[-1], lang)
        return rs[0] if len(rs)>0 else None

    def availble_langs(self):
        """
        $ python -m sagas.nlu.synonyms availble_langs
        :return:
        """
        import glob
        import ntpath
        prefix='/pi/stack/data/synonyms'
        files=glob.glob(f"{prefix}/*_def.yml")
        langs=[]
        for f in files:
            filename=(ntpath.basename(f))
            if filename[2]=='_':
                langs.append(filename[:2])

        return langs

synonyms=Synonyms()

if __name__ == '__main__':
    import fire
    fire.Fire(Synonyms)

