class SpacyExtractor(object):
    def __init__(self, model='en_core_web_sm'):
        import spacy
        self.nlp = spacy.load(model)

    # document level
    def entities_df(self, doc):
        import sagas
        rs = []
        for ent in doc.ents:
            rs.append((ent.text, ent.start_char, ent.end_char, ent.label_))
        return sagas.to_df(rs, ['word', 'start', 'end', 'entity'])

    # token level: https://spacy.io/api/token#attributes
    def token_entity_df(self, sents):
        import sagas
        doc = self.nlp(sents)
        rs = []
        for ent in doc:
            rs.append((ent.i, ent.idx, ent.text, ent.ent_type_, ent.ent_iob_,
                       [ent.is_punct, ent.like_num]))
        return sagas.to_df(rs, ['index', 'position', 'word', 'entity', 'iob', 'feat'])

    def to_df(self, text):
        """
        $ python -m sagas.nlu.extractor_spacy to_df 'Apple is looking at buying U.K. startup for $1 billion'
        :param text:
        :return:
        """
        doc = self.nlp(text)
        ents = [ent.label_.lower()[:3] + '_' + ent.text for ent in doc.ents]
        print("(%s)" % '; '.join(ents))
        print(self.entities_df(doc))

if __name__ == '__main__':
    import fire
    fire.Fire(SpacyExtractor)
