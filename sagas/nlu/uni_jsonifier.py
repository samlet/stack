from typing import Text, Any, Dict, List
from sagas.nlu.uni_cli import UniCli
from sagas.nlu.corenlp_parser import get_chunks
from sagas.tool.misc import print_stem_chunks
from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf, sent_jsonify
import sagas

def rs_summary(rs, console=True):
    from IPython.display import display
    import sagas
    for serial, r in enumerate(rs):
        df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
        if 'head' in r:
            cla = "%s(%s)" % (r['head'], r['head_pos'])
        else:
            cla = '_'
        print('%s(%s)' % (r['type'], r['lemma']), cla)
        # sagas.print_df(df)
        if not console:
            display(df)
        else:
            sagas.print_df(df)
        print_stem_chunks(r)

class JsonifyWordImpl(WordIntf):
    def setup(self, token):
        return token


class JsonifySentImpl(SentenceIntf):
    def setup(self, json_words):
        words = []
        # print(f'words count {len(json_words)}')
        for word in json_words:
            words.append(JsonifyWordImpl(word))
        return words, []

def jsonify_with(sents, lang, engine='corenlp'):
    doc= UniCli().parser(engine)(lang, sents)
    return sent_jsonify(doc)

def jsonify_pipelines(sents, lang, engine, pipelines):
    doc = UniCli().parser(engine)(lang, sents)
    return {'sents':sent_jsonify(doc),
            'predicts': doc.predicts}

class UniJsonifier(object):
    def viz_sample(self, lang:Text, sents:Text, engine='corenlp'):
        """
        $ python -m sagas.nlu.uni_jsonifier viz_sample ja "今何時ですか?"
        >>> viz_sample('ja', "今何時ですか?")
        :param lang:
        :param sents:
        :param engine:
        :return:
        """
        uni = UniCli()
        doc = uni.parser(engine)(lang, sents)
        # print(len(doc.words))
        words = sent_jsonify(doc)

        doc_jsonify = JsonifySentImpl(words, text=sents)
        rs = get_chunks(doc_jsonify)
        rs_summary(rs)

if __name__ == '__main__':
    import fire
    fire.Fire(UniJsonifier)
