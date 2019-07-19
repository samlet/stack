from natasha.markup import format_markup_css
from sagas.bots.hanlp_viz import to_df

class Matches(object):
    __attributes__ = ['text', 'matches']

    def __init__(self, text, matches, attrs=None):
        if attrs is None:
            attrs = ['nr']
        self.text = text
        # self.matches = sorted(matches, key=lambda _: _.span)
        # self.matches = sorted(r.entities, key=lambda _: _.start)
        self.matches=matches
        self.attrs=attrs

    def __iter__(self):
        return iter(self.matches)

    def __getitem__(self, index):
        return self.matches[index]

    def __len__(self):
        return len(self.matches)

    def __bool__(self):
        return bool(self.matches)

    # @property
    # def as_json(self):
    #     return [serialize(_) for _ in self.matches]

    def _repr_html_(self):
        spans = [(_.start,_.end) for _ in self.matches
                 if _.entity in self.attrs
                ]
        return ''.join(format_markup_css(self.text, spans))

def visual_sents(sents, attrs=None):
    """
    from sagas.bots.jupyter_tool import visual_sents
    visual_sents('我要找一本课本')
    :param sents:
    :return:
    """
    if attrs is None:
        attrs = ['nr', 'n']
    from IPython.display import display
    from sagas.bots.hanlp_viz import HanlpProtoViz, entities_df
    viz=HanlpProtoViz(verbose=False)
    # df = viz.deps_df(sents)
    # df = HanlpProtoViz().deps_df(sents)
    # display(df)

    ## entities
    r = viz.extract(sents)
    matches = sorted(r.entities, key=lambda _: _.start)
    display(entities_df(matches))
    m = Matches(sents, matches, attrs)
    display(m)

    ## dependency graph
    g=viz.analyse(sents)
    display(g)
    # g=HanlpProtoViz().analyse(sents)
    # display(g)








