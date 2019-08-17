from sagas.nlu.uni_impl_ltp import LtpParserImpl
from sagas.nlu.uni_impl_corenlp import CoreNlpParserImpl
from sagas.nlu.uni_impl_spacy import SpacyParserImpl

class UniCli(object):
    def __init__(self):
        self.parsers={'corenlp':lambda lang, sents: CoreNlpParserImpl(lang)(sents),
                      'ltp':lambda lang, sents: LtpParserImpl(lang)(sents),
                      'spacy':lambda lang, sents: SpacyParserImpl(lang)(sents),
                      }

    def parse(self, engine, lang, sents):
        """
        $ python -m sagas.nlu.uni_cli parse corenlp en 'it is a cat'
        $ python -m sagas.nlu.uni_cli parse ltp zh-CN '我送她一束花'
        $ python -m sagas.nlu.uni_cli parse spacy en 'it is a cat'
        :return:
        """
        from sagas.nlu.corenlp_parser import get_chunks
        import sagas
        from sagas.tool.misc import print_stem_chunks

        print(f'using engine {engine} ...')
        # parser = CoreNlpParserImpl('en')
        # doc = parser('it is a cat')
        doc=self.parsers[engine](lang, sents)
        rs = get_chunks(doc)
        for r in rs:
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
            print('%s(%s)' % (r['type'], r['lemma']))
            sagas.print_df(df)
            print_stem_chunks(r)

if __name__ == '__main__':
    import fire
    fire.Fire(UniCli)

