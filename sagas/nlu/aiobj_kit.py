from sagas.nlu.ruleset import result_df
from sagas.nlu.corenlp_parser import get_chunks
from sagas.nlu.uni_remote import dep_parse
from sagas.nlu.uni_remote_viz import list_chunks, display_doc_deps, list_rs
from sagas.nlu.inspector_fixtures import InspectorFixture
from sagas.tool.misc import color_print


def display_result_df(rs, presenter='jupyter'):
    df = result_df(rs)
    if presenter == 'jupyter':
        from IPython.display import display
        display(df)
    else:
        print(df)

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
    :param sents:
    :param lang:
    :param engine:
    :param options:
    :return:
    """
    from IPython.display import display

    if options is None:
        options=DomainGetOptions()
    pipelines=['predicts'] if options.enable_predicts else []
    doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
    result_set=[]
    if doc_jsonify is not None:
        color_print('cyan', resp)
        if resp is not None and 'predicts' in resp and len(resp['predicts'])>0:
            rs=resp['predicts']
            # print(rs)
        else:
            # print(doc_jsonify.words_string())
            rs = get_chunks(doc_jsonify)
        if len(rs)>0:
            if options.list_chunks:
                list_rs(rs)
            if options.deps_graph:
                display(display_doc_deps(doc_jsonify, resp))
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
                common = {'lemma': r['lemma'], 'stems': r['stems']}
                meta = {'rel': r['rel'], **common, **data}
                result_set.append((domains, meta))
        else:
            color_print('red', '.. no found predefined chunk-patterns.')
            print(doc_jsonify.words_string())
            print(doc_jsonify.dependencies_string())
    return result_set


