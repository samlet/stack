from sagas.nlu.ruleset import result_df
from sagas.nlu.corenlp_parser import get_chunks
from sagas.nlu.uni_remote import dep_parse
from sagas.nlu.uni_remote_viz import list_chunks, display_doc_deps, list_rs
from sagas.nlu.inspector_fixtures import InspectorFixture
# from sagas.tool.misc import color_print
import sagas.tracker_fn as tc

def display_result_df(rs):
    df = result_df(rs)
    # if presenter == 'jupyter':
    #     from IPython.display import display
    #     display(df)
    # else:
    #     print(df)
    tc.dfs(df)

fixture=InspectorFixture()

class DomainGetOptions(object):
    def __init__(self, enable_predicts=False, list_chunks=True, deps_graph=True):
        self.enable_predicts=enable_predicts
        self.list_chunks=list_chunks
        self.deps_graph=deps_graph


def get_domains(sents, lang, engine='corenlp', options=None):
    """
    >>> from sagas.nlu.aiobj_kit import get_domains
    >>> get_domains('你有几台笔记本电脑？', 'zh', 'ltp')
    >>> get_domains('列出上周编辑的文件。', 'zh', 'ltp', DomainGetOptions(enable_predicts=True))

    :param sents:
    :param lang:
    :param engine:
    :param options:
    :return:
    """
    # from IPython.display import display

    if options is None:
        options=DomainGetOptions()
    pipelines=['predicts'] if options.enable_predicts else []
    doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
    result_set=[]
    if doc_jsonify is not None:
        tc.emp('cyan', resp)
        if resp is not None and 'predicts' in resp and len(resp['predicts'])>0:
            rs=resp['predicts']
            # print(rs)
        else:
            # print(doc_jsonify.words_string())
            rs = get_chunks(doc_jsonify)
        if len(rs)>0:
            if options.list_chunks:
                list_rs(rs, lang)
            if options.deps_graph:
                # display(display_doc_deps(doc_jsonify, resp))
                tc.gv(display_doc_deps(doc_jsonify, resp,
                                       translit_lang=lang if lang in ('ja', 'ko', 'zh', 'fa', 'ar', 'he') else None))
            # rs_represent(rs, data = {'lang': lang, "sents": sents, 'engine': engine,
            #                         'pipelines':pipelines})
            data = {'lang': lang, "sents": sents, 'engine': engine,
                                     'pipelines':pipelines}
            for r in rs:
                # fixture.print_table(r, False)
                # print(f"lemma: {r['lemma']}")
                # df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
                # display(df)
                domains = r['domains']
                common = {'lemma': r['lemma'], 'word': r['word'],
                          'stems': r['stems']}
                meta = {'rel': r['rel'], **common, **data}
                result_set.append((domains, meta))
        else:
            tc.emp('red', '.. no found predefined chunk-patterns.')
            tc.info(doc_jsonify.words_string())
            tc.info(doc_jsonify.dependencies_string())
    return result_set


