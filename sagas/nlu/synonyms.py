import yaml

class Synonyms(object):
    def __init__(self):
        self.mappings={'id': self.load_dict('id')}

    def load_dict(self, lang):
        prefix = '/pi/stack/data/synonyms'
        file = f"{prefix}/{lang}_def.yml"
        with open(file, 'r') as f:
            return yaml.safe_load(f.read())

    def query(self, word, lang):
        """
        $ python -m sagas.nlu.synonyms query memulai id
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

synonyms=Synonyms()

if __name__ == '__main__':
    import fire
    fire.Fire(Synonyms)

