from sagas.ja.knp_helper import *

class KnpViz(object):
    """
    from sagas.ja.knp_viz import KnpViz
    >>> import sagas.ja.knp_helper as kh
    >>> kh.outputer='jupyter'
    >>> sent='久保氏は当初、連合を支持基盤とする民改連との連携を想定した。'
    >>> KnpViz().process_tags(sent)
    >>> KnpViz().process('私の趣味は、多くの小旅行をすることです。')
    """
    def __init__(self, shape='egg', size='8,5', fontsize=0, verbose=False):
        from graphviz import Digraph
        self.verbose=verbose
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize != 0:
            self.f.attr(fontsize=str(fontsize))

        self.prop_sets = {'VERB': lambda f: f.attr('node', style='filled', color='lightgrey'),
                          'PRON': lambda f: f.attr('node', style='dashed', color='red'),
                          'AUX': lambda f: f.attr('node', style='dashed', color='green'),
                          'NOUN': lambda f: f.attr('node', style='solid', color='blue'),
                          }

    def default_node(self):
        self.f.attr('node', style='solid', color='black')

    def process_tags(self, sents):
        result = knp.parse(sents)
        print(sents)
        # deps, predicates, _ = print_predicates(result)
        deps, predicates, _, _ = extract_predicates(result)
        self.prop_sets['VERB'](self.f)
        for pr in predicates:
            self.f.node(pr)

        self.default_node()
        # establish_set = {}

        rs = []
        words = result.tag_list()
        for tag in words:  # 各基本句へのアクセス
            if self.verbose:
                print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s" \
                      % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id,
                         tag.fstring))
            node_text = merge_tag(tag)
            rs.append((tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()),
                       ",".join(pos_list(tag)),
                       ','.join(pos_map_list(tag)),
                       ",".join(entity_list(tag)),
                       tag.dpndtype, tag.parent_id, tag.fstring))
            rel = tag.dpndtype
            if tag.parent_id == -1:
                head_node = 'ROOT'
            else:
                head_node = merge_tag(words[tag.parent_id])
                rel = get_by_keyset(deps, {tag.tag_id, tag.parent_id})
                # print(tag.tag_id, tag.parent_id, {tag.tag_id, tag.parent_id}, rel)
                if rel is None:
                    rel = tag.dpndtype
                else:
                    remove_by_keyset(deps, {tag.tag_id, tag.parent_id})
            self.f.edge(head_node, node_text, label=rel, fontsize='11', fontname='Calibri')

        display(sagas.to_df(rs, ['ID', '見出し', 'POS', 'UPOS', 'Entities',
                                 '係り受けタイプ(dep_type)', '親基本句ID', '素性']))
        print('leaves', deps)
        return self.f

    def process(self, sents):
        result = knp.parse(sents)
        print(sents)
        # print_predicates(result)
        extract_predicates(result)

        rs = []
        words = result.bnst_list()
        for bnst in words:  # 各文節へのアクセス
            if self.verbose:
                print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s" \
                      % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id,
                         bnst.fstring))
            node_text = merge_chunk(bnst)
            rs.append((bnst.bnst_id, node_text,
                       ",".join(pos_list(bnst)),
                       ','.join(pos_map_list(bnst)),
                       ",".join(entity_list(bnst)),
                       bnst.dpndtype, bnst.parent_id, bnst.fstring))
            if bnst.parent_id == -1:
                head_node = 'ROOT'
            else:
                head_node = merge_chunk(words[bnst.parent_id])
            self.f.edge(head_node, node_text, label=bnst.dpndtype, fontsize='11', fontname='Calibri')
        display(sagas.to_df(rs, ['ID', '見出し', 'POS', 'UPOS', 'Entities',
                                 '係り受けタイプ(dep_type)', '親文節ID', '素性']))
        return self.f

