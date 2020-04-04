from sagas.nlu.anal import build_anal_tree
from sagas.nlu.ruleset_procs import cached_chunks
from sagas.nlu.utils import fix_sents
from sagas.nlu.nlu_tools import treeing
from sagas.nlu.features import get_feats_map, feats_map
from anytree import Node, RenderTree, AsciiStyle, Walker, Resolver
from anytree.importer import DictImporter
from anytree.search import findall, findall_by_attr
from sagas.nlu.translator import get_contrast
import pandas as pd
import sagas.tracker_fn as tc

importer = DictImporter()

def proc_verb_subs(node):
    toks = findall_by_attr(node, name='dependency_relation', value='nsubj')
    if not toks:
        toks = findall_by_attr(node, name='dependency_relation', value='dislocated')
    if toks:
        tok = toks[0]
        objs = findall(node, filter_=lambda n: n.dependency_relation in ("obj"))
        if objs:
            print(f'✔[verb-{tok.dependency_relation}-obj]',
                  node.text, tok.text, objs[0].text)
            return True
        objs = findall_by_attr(node, name='upos', value='NOUN')
        # objs=findall(f, filter_=lambda node: node.upos in ("NOUN", "ADJ"))
        if objs:
            print(f'✔[verb-{tok.dependency_relation}-noun]', node.text, tok.text,
                  objs[0].dependency_relation, objs[0].text)
            return True
    return False

def domains_as_tree(sents, lang, engine='stanza', domain='root_domains'):
    chunks = cached_chunks(sents,
                           source=lang,
                           engine=engine)
    root = chunks[domain]
    ds = treeing(root[0])
    f = importer.import_(ds)
    return f

def digest_verb(sents, lang, engine='stanza'):
    f=build_anal_tree(sents, lang, engine)
    words = findall_by_attr(f, name='upos', value='VERB')
    if words:
        print(sents, len(words))
        rs = []
        for w in words:
            rs.append(proc_verb_subs(w))

        def proc_text(t):
            if lang in ('ko'):
                return get_contrast(t, lang)
            return t
        succ=any(rs)
        cl='blue' if succ else 'white'
        tc.emp(cl, RenderTree(f, style=AsciiStyle()).by_attr(
            lambda n: f"{n.dependency_relation}: {proc_text(n.text)} {n.upos}"))
        return succ
    return False


def proc_corpus(lang, chapter):
    """
    >>> proc_corpus('ko', 'At school')
    :param lang:
    :param chapter:
    :return:
    """
    dfjson = pd.read_json(f'~/pi/stack/crawlers/langcrs/all_{lang}.json')
    ch = dfjson[dfjson['chapter'].str.match(chapter)]
    rs_map = {}
    for i, (sent, ref) in enumerate(zip(ch['translate'], ch['text'])):
        text = fix_sents(sent, lang)
        print('-', i, ref, '-' * 10)
        # digest(text, 'spacy')
        rs_map[i] = digest_verb(text, lang, 'stanza')
    return len(ch), len([t for t in rs_map.values() if t])

class AnalCorpus(object):
    def chapters(self):
        """
        $ python -m sagas.nlu.anal_corpus chapters
        :return:
        """
        def list_chapter_titles(lang):
            dfjson = pd.read_json(f'~/pi/stack/crawlers/langcrs/all_{lang}.json')
            return [name for name, group in dfjson.groupby('chapter')]

        return list_chapter_titles('es')

    def corpus(self, lang, chapter):
        """
        $ python -m sagas.nlu.anal_corpus corpus ko 'At school'
        :param lang:
        :param chapter:
        :return:
        """
        total, parsed= proc_corpus(lang, chapter)
        print(f"total {total}, parsed {parsed}")

if __name__ == '__main__':
    import fire
    fire.Fire(AnalCorpus)
