from sagas.nlu.uni_viz import EnhancedViz
from sagas.nlu.corenlp_parser import get_chunks
from sagas.tool.misc import print_stem_chunks
import sagas

serial_numbers='❶❷❸❹❺❻❼❽❾❿'

def list_rs(rs):
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
        # print(resp)

def list_chunks(doc_jsonify, resp):
    if len(resp['predicts']) > 0:
        rs=resp['predicts']
    else:
        rs = get_chunks(doc_jsonify)
    list_rs(rs)

def display_doc_deps(doc_jsonify, resp):
    from termcolor import colored
    print(colored(f"✁ dependency-graph. {'-' * 25}", 'cyan'))
    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    return cv.analyse_doc(doc_jsonify, None, console=False)

def viz_sample(lang, sents, engine='corenlp'):
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
    list_chunks(doc_jsonify, resp)
    return display_doc_deps(doc_jsonify, resp)



