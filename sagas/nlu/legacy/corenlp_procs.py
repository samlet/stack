import sagas
def words_table(sents, lang):
    from sagas.nlu.corenlp_helper import get_nlp
    nlp=get_nlp(lang)
    doc = nlp(sents)
    sentence=doc.sentences[0]
    rows=[[word.text, word.lemma, word.upos, word.xpos,
           word.dependency_relation, word.governor,
           word.feats] for word in sentence.words]
    return sagas.to_df(rows, ['text','lemma', 'upos', 'xpos', 'dep', 'head', 'feats'])

class CorenlpProcs(object):
    def testings(self):
        """
        $ python -m sagas.nlu.corenlp_procs testings
        :return:
        """
        ds=[words_table('عمري تسعة عشر عاماً.', 'ar'),
            words_table('آخرین کسی که به کامپیوتر وصل شد، کی بود؟', 'fa')
            ]
        for df in ds:
            sagas.print_df(df)

if __name__ == '__main__':
    import fire
    fire.Fire(CorenlpProcs)
