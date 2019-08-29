from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf
import sagas.ja.knp_helper as kh
from sagas.ja.knp_helper import *

def tag_pos(tag, only_first=True):
    if only_first:
        return kh.pos_map_list(tag)[0]
    return '_'.join(kh.pos_map_list(tag))

class KnpWordImpl(WordIntf):
    def __init__(self, data, deps):
        self.deps = deps
        super().__init__(data)

    def setup(self, tag):
        if tag.parent_id == -1:
            governor = 0
        else:
            governor = tag.parent_id + 1
        idx = tag.tag_id + 1  # start from 1
        text = "".join(mrph.midasi for mrph in tag.mrph_list())
        lemma = tag.mrph_list()[0].midasi
        rel = get_by_keyset(self.deps, {tag.tag_id, tag.parent_id})
        if rel is None:
            rel = tag.dpndtype
        features = {'index': idx, 'text': text, 'lemma': lemma,
                    'upos': tag_pos(tag), 'xpos': pos_list(tag),
                    'feats': [tag.fstring], 'governor': governor,
                    'dependency_relation': rel,
                    'entity': entity_list(tag)
                    }
        return features


class KnpSentImpl(SentenceIntf):
    def __init__(self, sent, predicts, dep_sets):
        self.dep_sets = dep_sets
        super(KnpSentImpl, self).__init__(sent, predicts)

    def setup(self, sent):
        words = []
        for tag in sent.tag_list():
            words.append(KnpWordImpl(tag, self.dep_sets))
        deps = []
        return words, deps


class KnpParserImpl(object):
    """
    >>> from sagas.nlu.uni_viz_checker import *
    >>> viz_check(KnpParserImpl, 'ja', '私の趣味は、多くの小旅行をすることです。')
    """
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents):
        result = kh.knp.parse(sents)
        dep_sets, predict_keys, predicts = print_predicates(result, verbose=False)
        return KnpSentImpl(result, predicts, dep_sets=dep_sets)

