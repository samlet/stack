import sagas
from pyknp import KNP
from sagas.util.pandas_helper import crop_column

knp = KNP()
outputer='console'

upos_maps={'形容詞':'ADJ', '副詞':'ADV',
           '接続詞':'CCONJ', '連体詞':'DET',
           '感動詞':'INTJ', '名詞':'NOUN', '名詞-数詞':'NUM',
           '代名詞':'PRON', '名詞-固有名詞':'PROPN',
           '補助記号':'PUNCT',
           '動詞':'VERB', '未定義語':'X'
          }
upos_rev_maps={'PUNCT':['特殊-句点', '特殊-読点'],
               'SYM':['補助記号', '補助記号-一般', '補助記号-ＡＡ-顔文字'],
               'ADP':['助詞-格助詞', '助詞-係助詞'],
               'AUX':['助動詞', '動詞-非自立可能', '形容詞-非自立可能'],
               'SCONJ':['接続詞', '助詞-接続助詞','助詞-準体助詞'],
               'CCONJ':['助詞-格助詞','助詞-格助詞', '助詞-副助詞'],
               'PART':['助詞-終助詞', '接尾辞-形状詞的']}

def get_pos_mapping(pos1, pos2, default_val='X'):
    for pos in [f"{pos1}-{pos2}", pos1]:
        if pos in upos_maps:
            return upos_maps[pos]
        else:
            for k, v in upos_rev_maps.items():
                if pos in v:
                    return k
    return default_val

POS_MARK = {
    '特殊': '*',
    '動詞': 'v',
    '形容詞': 'j',
    '判定詞': 'c',
    '助動詞': 'x',
    '名詞': 'n',
    '固有名詞': 'N',
    '人名': 'J',
    '地名': 'C',
    '組織名': 'A',
    '指示詞': 'd',
    '副詞': 'a',
    '助詞': 'p',
    '接続詞': 'c',
    '連体詞': 'm',
    '感動詞': '!',
    '接頭辞': 'p',
    '接尾辞': 's',
    '未定義語': '?'
}
ner_mappings={'固有名詞':'MISC',
              '人名':'PERSON', '地名':'LOC',
              '組織名':'ORG'}

def pos_list(leaf):
    import re
    string=[]
    for mrph in leaf.mrph_list():
        # string += mrph.midasi
        # bunrui (str): 品詞細分類
        # hinsi (str): 品詞
        if re.search("^(?:固有名詞|人名|地名)$", mrph.bunrui):
            string.append(POS_MARK[mrph.bunrui])
        else:
            string.append(POS_MARK[mrph.hinsi])
    return string

def pos_map_list(leaf):
    string=[]
    for mrph in leaf.mrph_list():
        string.append(get_pos_mapping(mrph.hinsi, mrph.bunrui))
    return string

def entity_list(leaf):
    import re
    string=[]
    for mrph in leaf.mrph_list():
        if mrph.bunrui in ner_mappings:
            string.append(ner_mappings[mrph.bunrui])
    return string

def get_segments(leaf):
    segs=[]
    for mrph in leaf.mrph_list():
        seg={}
        seg['index']=mrph.mrph_id
        seg['upos']=get_pos_mapping(mrph.hinsi, mrph.bunrui)
        seg['xpos'] = [mrph.hinsi, mrph.bunrui]
        seg['text'] = mrph.midasi
        if mrph.repname:
            lemmas=mrph.repname.split('/')
            if len(lemmas)>0:
                seg['lemmas']=lemmas
        if mrph.bunrui in ner_mappings:
            seg['entity']=ner_mappings[mrph.bunrui]
        segs.append(seg)
    return segs

def display(df, col_defs=None):
    if outputer=='console':
        if col_defs is not None:
            for col in col_defs:
                crop_column(df, col[0], col[1])
        sagas.print_df(df)
    else:
        from IPython.display import display
        display(df)

def parse_knp(sents, verbose=False):
    result = knp.parse(sents)
    print("文節")
    rs=[]
    col_defs=[('素性', 20)]
    for bnst in result.bnst_list(): # 各文節へのアクセス
        if verbose:
            print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s" \
                    % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))
        rs.append((bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))
    display(sagas.to_df(rs, ['ID', '見出し', '係り受けタイプ(dep_type)', '親文節ID', '素性']), col_defs)

    print("基本句")
    rs=[]
    for tag in result.tag_list(): # 各基本句へのアクセス
        if verbose:
            print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s" \
                    % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring))
        rs.append((tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()),
                   ",".join(pos_list(tag)),
                   ','.join(pos_map_list(tag)),
                   ",".join(entity_list(tag)),
                   tag.dpndtype, tag.parent_id, tag.fstring))
    display(sagas.to_df(rs, ['ID', '見出し', 'POS', 'UPOS', 'Entities',
                             '係り受けタイプ', '親基本句ID', '素性']), col_defs)

    print("形態素")
    rs=[]
    for mrph in result.mrph_list(): # 各形態素へのアクセス
        if verbose:
            print("\tID:%d, 見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
                    % (mrph.mrph_id, mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
        rs.append((mrph.mrph_id, mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
    display(sagas.to_df(rs, 'ID:%d, 見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s'.split(', ')))

def put_items(some_map, keyset, val):
    keystr=':'.join([str(k) for k in sorted(keyset)])
    some_map[keystr]=val
def get_by_keyset(some_map, keyset):
    keystr=':'.join([str(k) for k in sorted(keyset)])
    # print(keystr)
    if keystr in some_map:
        return some_map[keystr]
    return None
def remove_by_keyset(some_map, keyset):
    keystr=':'.join([str(k) for k in sorted(keyset)])
    del some_map[keystr]

def merge_chunk(bnst):
    chunk="".join(mrph.midasi for mrph in bnst.mrph_list())
    tag_size=len(bnst.tag_list())
    return f"{chunk}({tag_size})"
def merge_tag(tag):
    chunk=", ".join(mrph.midasi for mrph in tag.mrph_list())
    return chunk

# def print_predicates(result, verbose=True):
#     deps={}
#     predict_keys=[]
#     predicts=[]
#     for tag in result.tag_list():
#         if tag.pas is not None:  # find predicate
#             predict_cnt=''.join(mrph.midasi for mrph in tag.mrph_list())
#             if verbose:
#                 print(tag.tag_id, '. 述語: %s' % predict_cnt)
#             predict_keys.append(merge_tag(tag))
#             p_args=[]
#             for case, args in tag.pas.arguments.items():  # case: str, args: list of Argument class
#                 for arg in args:  # arg: Argument class
#                     if verbose:
#                         print('\t格: %s,  項: %s  (項の基本句ID: %d)' % (case, arg.midasi, arg.tid))
#                     put_items(deps, {tag.tag_id, arg.tid}, case)
#                     p_args.append({'name':case, 'value':arg.midasi, 'start':arg.tid, 'end':arg.tid})
#             predicts.append({'index':tag.tag_id, 'predicate':predict_cnt, 'args':p_args})
#     if verbose:
#         print(deps, predict_keys)
#         print(predicts)
#     return deps, predict_keys, predicts

def trim_chunk(chunk):
    return [c for c in chunk if c != '']

def tag_pos(tag, only_first=True):
    if only_first:
        return pos_map_list(tag)[0]
    return '_'.join(pos_map_list(tag))

def get_feats(tag):
    return ['c_{}'.format(tag_pos(tag)).lower(),
            'x_{}'.format(pos_list(tag)[0]).lower()]


def get_governor(tag):
    if tag.parent_id == -1:
        governor = 0
    else:
        governor = tag.parent_id + 1
    return governor


def collect_bnst(result):
    rs = []
    for bnst in result.bnst_list():
        rs.append(([tag.tag_id for tag in bnst.tag_list()],
                   [mrph.repname.split('/')[0] for mrph in bnst.mrph_list()]
                   ))
    return rs


def extract_predicates(result, verbose=True):
    deps = {}
    predict_keys = []
    predicts = []
    predict_tuples = []
    bnst_set = collect_bnst(result)
    words = result.tag_list()
    for tag in words:
        if tag.pas is not None:  # find predicate
            predict_cnt = ''.join(mrph.midasi for mrph in tag.mrph_list())
            # word_main=tag.mrph_list()[0]
            if verbose:
                print(tag.tag_id, '. 述語: %s' % predict_cnt)
            # print(tag.features)
            # print(tag.normalized_repname)

            repname = tag.normalized_repname.split('/')
            predict_lemma = repname[0]
            predict_phonetic = repname[1] if len(repname) > 1 else predict_lemma

            predict_keys.append(merge_tag(tag))
            p_args = []
            domains = []
            for case, args in tag.pas.arguments.items():  # case: str, args: list of Argument class
                for arg in args:  # arg: Argument class
                    arg_tag = words[arg.tid]
                    if verbose:
                        print('\t格: %s,  項: %s  (項の基本句ID: %d)' % (case, arg.midasi, arg.tid))
                    put_items(deps, {tag.tag_id, arg.tid}, case)
                    cnt = ''.join(mrph.midasi for mrph in arg_tag.mrph_list())
                    chunk = [b[1] for b in bnst_set if arg_tag.tag_id in b[0]][0]
                    p_args.append({'name': case, 'value': arg.midasi, 'text': cnt,
                                   'chunk': chunk,
                                   'upos': tag_pos(arg_tag),
                                   'start': arg.tid, 'end': arg.tid})
                    # ['rel', 'index', 'text', 'lemma', 'children', 'features']
                    feats = get_feats(arg_tag)
                    domains.append((case, arg.tid, cnt, arg.midasi, trim_chunk(chunk), feats))
            predicts.append({'index': tag.tag_id, 'predicate': predict_lemma,
                             'cnt': predict_cnt, 'phonetic': predict_phonetic,
                             'args': p_args})
            predict_tuples.append({'type': 'predicate', 'lemma': predict_lemma, 'index': tag.tag_id,
                                   'phonetic': predict_phonetic, 'word':predict_cnt,
                                   'rel': tag.dpndtype, 'governor': get_governor(tag),
                                   'pos': tag_pos(tag).lower(),
                                   'domains': domains, 'stems': [],
                                   'segments': get_segments(tag)})
    if verbose:
        print(deps, predict_keys)
        # print(predicts)
    return deps, predict_keys, predicts, predict_tuples


def tokens(sents):
    result = knp.parse(sents)
    return [mrph.midasi for bunsetsu in result for mrph in bunsetsu.mrph_list()]
