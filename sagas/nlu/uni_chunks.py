from sagas.nlu.inspector_path import normal_path
from jsonpath_ng import jsonpath, parse

def index_for_path(path):
    prefix = '$.'
    suffix = '.index'
    parts = path.split('/')
    parts_str = '.'.join([f"{t}[*]" for t in parts])
    return f"{prefix}{parts_str}{suffix}"


def get_index_with(chunks, domain_name, expr):
    parser = parse(index_for_path(expr))
    # chunk=chunks['verb_domains'][0]
    for chunk in chunks[domain_name]:
        idx = '/'.join([match.value for match in parser.find(chunk)])
        if idx != '':
            return idx
    return None


def it_children_cl(sent, word, rs, clo):
    equals = lambda a, b: str(a) == str(b)
    for c in filter(lambda w: equals(w.governor, word.index), sent.words):
        rs.append((c.index, clo(c)))
        it_children_cl(sent, c, rs, clo)


def get_children_cl(sent, word, clo):
    rs = []
    it_children_cl(sent, word, rs, clo)
    rs.append((word.index, clo(word)))
    # sort by word's index
    rs = sorted(rs, key=lambda _: int(_[0]))
    result = [w[1] for w in rs]
    return result


def get_chunk(chunks, domain_name, expr, clo=None):
    """
    子句复合成份提取
    See also: procs-parse-free.ipynb
    >>> from sagas.nlu.uni_chunks import get_chunk
        from sagas.nlu.ruleset_procs import list_words, cached_chunks
        from sagas.conf.conf import cf
        # get_chunk(f'verb_domains', 'xcomp/obj', lambda w: w.upos)
    >>> chunks = cached_chunks(sents, lang, cf.engine(lang))
    >>> result=get_chunk(chunks, f'{domain}_domains', 'xcomp/obj', lambda w: (w.text, w.upos.lower()))

    :param chunks:
    :param domain_name:
    :param expr:
    :param clo:
    :return:
    """
    idx = get_index_with(chunks, domain_name, expr)
    if clo is None:
        clo = lambda w: w.text
    if idx:
        sent_p = chunks['doc']
        root = next(w for w in sent_p.words if w.index == idx)
        # wlist=get_children_list(sent_p, root, include_self=True, stem=False)
        wlist = get_children_cl(sent_p, root, clo)
        return wlist
    return []

