from sagas.nlu.uni_impl_knp import KnpParserImpl
from sagas.nlu.uni_impl_ltp import LtpParserImpl
from sagas.nlu.uni_impl_corenlp import CoreNlpParserImpl
from sagas.nlu.uni_impl_spacy import SpacyParserImpl
from sagas.nlu.uni_impl_hanlp import HanlpParserImpl

class UniCli(object):
    def __init__(self):
        self.parsers={'corenlp':lambda lang, sents: CoreNlpParserImpl(lang)(sents),
                      'ltp':lambda lang, sents: LtpParserImpl(lang)(sents),
                      'spacy':lambda lang, sents: SpacyParserImpl(lang)(sents),
                      'hanlp':lambda lang, sents: HanlpParserImpl(lang)(sents),
                      'knp':lambda lang, sents: KnpParserImpl(lang)(sents),
                      }

    def parse(self, engine, lang, sents):
        """
        $ python -m sagas.nlu.uni_cli parse corenlp en 'it is a cat'
        $ python -m sagas.nlu.uni_cli parse ltp zh-CN '我送她一束花'
        $ python -m sagas.nlu.uni_cli parse hanlp zh-CN '我送她一束花'
        $ python -m sagas.nlu.uni_cli parse spacy en 'it is a cat'
        $ python -m sagas.nlu.uni_cli parse knp ja '私の趣味は、多くの小旅行をすることです。'
        :return:
        """
        from sagas.nlu.corenlp_parser import get_chunks
        import sagas
        from sagas.tool.misc import print_stem_chunks
        from sagas.tool.misc import color_print

        print(f'using engine {engine} ...')
        # parser = CoreNlpParserImpl('en')
        # doc = parser('it is a cat')
        doc=self.parsers[engine](lang, sents)
        color_print('blue', doc.predicts)
        rs = get_chunks(doc)
        for r in rs:
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
            print('%s(%s)' % (r['type'], r['lemma']))
            sagas.print_df(df)
            print_stem_chunks(r)

def parse_with(sents, lang, engine='corenlp'):
    return UniCli().parsers[engine](lang, sents)

if __name__ == '__main__':
    import fire
    fire.Fire(UniCli)

