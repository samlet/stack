from sagas.nlu.uni_viz import EnhancedViz
from sagas.nlu.corenlp_parser import get_chunks
from sagas.tool.misc import print_stem_chunks, display_synsets, proc_word, proc_children_column
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

def list_contrast(rs, lang):
    result=[]
    for serial, r in enumerate(rs):
        type_name = r['type']
        df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
        result.extend(proc_word(type_name, r['word'],
                                r['head'] if 'head' in r else '',
                                lang))
        result.extend(proc_children_column(df['rel'], df['children'], lang))
    return result

def list_chunks(doc_jsonify, resp, lang, enable_contrast=False):
    if len(resp['predicts']) > 0:
        rs=resp['predicts']
    else:
        rs = get_chunks(doc_jsonify)
    list_rs(rs, lang)
    if enable_contrast:
        _=list_contrast(rs, lang)
        # for c in contras:
        #     print(c)

def display_doc_deps(doc_jsonify, resp, translit_lang=None):
    from termcolor import colored
    print(colored(f"✁ dependency-graph. {'-' * 25}", 'cyan'))
    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20, translit_lang=translit_lang)
    return cv.analyse_doc(doc_jsonify, None, console=False)

def viz_sample(lang, sents, engine='corenlp', translit_lang=None, enable_contrast=False):
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
    list_chunks(doc_jsonify, resp, lang, enable_contrast=enable_contrast)
    return display_doc_deps(doc_jsonify, resp, translit_lang=translit_lang)



