import logging
logger = logging.getLogger(__name__)

def traverse(dict_or_list, path=[]):
    if isinstance(dict_or_list, dict):
        iterator = dict_or_list.items()
    else:
        iterator = enumerate(dict_or_list)
    for k, v in iterator:
        yield path + [k], v
        if isinstance(v, (dict, list)):
            for k, v in traverse(v, path + [k]):
                yield k, v


def iter_type(spec, el, attr=None):
    """
    >>> el=domains[0]
    >>> items=iter_type(dict, el, 'text')
    >>> _=iter_type(str, el)

    :param spec:
    :param el:
    :param attr:
    :return:
    """
    rs_map={}
    for path, node in traverse(el):
        if isinstance(node, spec):
            logger.debug(path, node if attr is None else node[attr])
            rs_map[tuple(path)]=node
    return rs_map

def vis_domains(sents, lang, domain):
    """
    >>> sents='What do you think about the war?'
    >>> lang='en'
    >>> domain='subj_domains' # 'verb_domains', 'aux_domains'
    >>> vis_domains(sents, lang, domain)

    :param sents:
    :param lang:
    :param domain:
    :return:
    """
    from sagas.nlu.ruleset_procs import cached_chunks
    from sagas.conf.conf import cf
    from sagas.kit.viz_base import BaseViz

    chunks = cached_chunks(sents, lang, cf.engine(lang))
    domains = chunks[domain]
    if len(domains)==0:
        return None

    el = domains[0]
    el_root = el['text']
    items = iter_type(dict, el, 'text')

    viz = BaseViz()
    print('.. root', el_root)
    viz.node(el_root, True)
    for e in items.keys():
        if e[0] == 'dc':
            dc = el['dc']['text']
            viz.node(dc, True)
            viz.edge(dc, el_root, domain.replace('_', '.'))
        else:
            head = 'root' if len(e) == 2 else e[0:-2]
            print(e, '->', head)
            print('\t', items[e]['text'], items[head]['text'] if head != 'root' else 'root', '.'.join(map(str, e)))
            viz.edge(items[head]['text'] if head != 'root' else el_root,
                     items[e]['text'],
                     '.'.join(map(str, e)))

    return viz.f

def vis_doc(sents, lang):
    from sagas.nlu.ruleset_procs import cached_chunks
    from sagas.nlu.uni_remote_viz import list_contrast, display_doc_deps
    from sagas.conf.conf import cf

    chunks = cached_chunks(sents, lang, cf.engine(lang))
    return display_doc_deps(chunks['doc'], None)

