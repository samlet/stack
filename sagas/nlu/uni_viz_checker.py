from sagas.nlu.uni_viz import EnhancedViz
from sagas.nlu.corenlp_parser import get_chunks
from sagas.tool.misc import print_stem_chunks
import sagas

serial_numbers='❶❷❸❹❺❻❼❽❾❿'

def viz_check(parser, lang, sents):
    """
    >>> from sagas.nlu.uni_impl_hanlp import HanlpParserImpl
    >>> # from sagas.nlu.uni_viz_checker import *
    >>> parser=HanlpParserImpl
    >>> viz_check(parser, 'zh', '我必须关掉房间里的灯。')
    >>> from sagas.nlu.uni_impl_knp import KnpParserImpl
    >>> viz_check(KnpParserImpl, 'ja', '私の趣味は、多くの小旅行をすることです。')
    :param parser:
    :param lang:
    :param sents:
    :return:
    """
    from IPython.display import display

    doc = parser(lang)(sents)
    rs = get_chunks(doc)

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

    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    return cv.analyse_doc(doc, None)

