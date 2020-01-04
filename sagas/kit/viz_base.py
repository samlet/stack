class BaseViz(object):
    def __init__(self, shape='egg', size='8,5', fontsize=0, enable_node_pos=False, translit_lang=None):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize != 0:
            self.f.attr(fontsize=str(fontsize))
        self.enable_node_pos = enable_node_pos
        self.translit_lang = translit_lang

    def default_node(self):
        self.f.attr('node', style='solid', color='black')

    def edge(self, head, node, rel):
        self.f.edge(head, node,
                    rel, fontsize='10', fontname='Calibri')

    def node(self, text, emphasis=False):
        if emphasis:
            self.f.attr('node', style='filled', color='lightgrey')
        self.f.node(text)
        if emphasis:
            self.default_node()


