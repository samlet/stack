from sagas.nlu.uni_viz import EnhancedViz
from sagas.nlu.corenlp_parser import get_chunks
from sagas.tool.misc import print_stem_chunks, display_synsets
import sagas

serial_numbers='❶❷❸❹❺❻❼❽❾❿'

def list_synsets(r, lang):
    # create a meta structure
    common = {'lemma': r['lemma'], 'stems': r['stems']}
    meta = {'rel': r['rel'], 'lang': lang, **common}
    if 'head' in r:
        meta['head'] = r['head']
    display_synsets(r['type'], meta, r, lang)

def list_rs(rs, lang):
    from IPython.display import display
    from termcolor import colored
    print(colored(f"✁ chunks. {'-' * 25}", 'cyan'))
    for serial, r in enumerate(rs):
        df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
        if 'head' in r:
            cla = "%s(%s)" % (r['head'], r['head_pos'])
        else:
            cla = '_'
        print(serial_numbers[serial], '%s(%s)' % (r['type'], r['lemma']), cla)
        # sagas.print_df(df)
        display(df)
        print_stem_chunks(r)
        list_synsets(r, lang)

        # print(resp)

def list_chunks(doc_jsonify, resp, lang):
    if len(resp['predicts']) > 0:
        rs=resp['predicts']
    else:
        rs = get_chunks(doc_jsonify)
    list_rs(rs, lang)

def display_doc_deps(doc_jsonify, resp, translit_lang=None):
    from termcolor import colored
    print(colored(f"✁ dependency-graph. {'-' * 25}", 'cyan'))
    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20, translit_lang=translit_lang)
    return cv.analyse_doc(doc_jsonify, None, console=False)

def viz_sample(lang, sents, engine='corenlp', translit_lang=None):
    """
    >>> from sagas.nlu.uni_remote_viz import viz_sample
    >>> sents='what time is it ?'
    >>> viz_sample('en', sents)

    en="I have to turn off the lights in the room."
    zh="我必须关掉房间里的灯。"
    ja="部屋の明かりを消さなければなりません。"
    viz_sample('en', en)

    :param lang:
    :param sents:
    :param engine:
    :return:
    """
    # uni=UniCli()
    # doc=uni.parsers[engine](lang, sents)
    from sagas.nlu.uni_remote import dep_parse
    doc_jsonify, resp = dep_parse(sents, lang, engine, ['predicts'])
    if doc_jsonify is None:
        raise Exception(f'Cannot parse sentence for lang {lang}')
    list_chunks(doc_jsonify, resp, lang)
    return display_doc_deps(doc_jsonify, resp, translit_lang=translit_lang)



