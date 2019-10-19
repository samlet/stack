from sagas.nlu.utils import fix_sents
from sagas.conf.conf import cf
from sagas.nlu.uni_remote import dep_parse
from sagas.nlu.corenlp_parser import get_chunks
import sagas
import json
from sagas.nlu.uni_remote_viz import list_synsets

def parse_comps(sents, source):
    sents=fix_sents(sents, source)

    engine=cf.engine(source)
    doc_jsonify, resp = dep_parse(sents, source, engine, ['predicts'])
    if len(resp['predicts']) > 0:
        rs=resp['predicts']
    else:
        rs = get_chunks(doc_jsonify)
    return rs

def make_map(partcol, textcol):
    return dict(zip(partcol, textcol))
def list_contrast(rs, lang):
    result=[]
    for serial, r in enumerate(rs):
        type_name = r['type']
        df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
        rec={'type':type_name, 'word':r['word'], 'head': r['head'] if 'head' in r else ''}
        rec['domains']=make_map(df['rel'], df['children'])
        rec['synsets']=list_synsets(r, lang, True)
        result.append(rec)
    return result

def procs_sents(sents, source):
    """
    sents='彼女は 美人な だけでなく 、 頭も いい です 。'
    source='ja'
    procs_sents(sents, source)

    :param sents:
    :param source:
    :return:
    """
    rs=parse_comps(sents, source=source)
    result=list_contrast(rs, source)
    return result

