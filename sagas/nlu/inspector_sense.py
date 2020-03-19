from sagas.nlu.inspector_common import Inspector, Context


class SenseInspector(Inspector):
    """
    Instances: sense('obj').cat_of(obj='SportTool|运动器材')
       .has_role(domain='football|足球')
       .has_role(domain='sport|体育')
       .has_role(CoEvent='exercise|锻炼'),

    Examples:
        >>> from sagas.nlu.parse_client_helper import build_context
        >>> from sagas.nlu.rules_header import *
        >>>
        >>> data={'lang': 'en', "sents": 'i play football'}
        >>> ctx,pat=next(build_context(data, 'verb', name='_test_', engine='corenlp'))
        >>> print(ctx.engine)
        >>>
        >>> rs=pat(sense('obj').cat_of(obj='SportTool|运动器材')
        >>>        .has_role(domain='football|足球')
        >>>        .has_role(domain='sport|体育')
        >>>        .has_role(CoEvent='exercise|锻炼'),
        >>>        obj=kindof('football', 'n'))
        >>> (rs[1], rs[0])
    """
    def __init__(self, arg=''):
        self.arg=arg
        self.opts = {}
        self.routines=[]
    def name(self):
        return "sense"

    def cat_of(self, **kwargs):
        def fn(key, ctx:Context):
            from sagas.zh.hownet_helper import get_word_sense, get_trees
            results=[]
            for k,v in kwargs.items():
                word=ctx.words[k]
                sts = get_trees(word)
                results.append(any([st.cat_of(v) for st in sts]))
            return all(results)
        self.routines.append(fn)
        return self

    def has_role(self, **roles):
        def fn(key, ctx:Context):
            from sagas.zh.hownet_helper import get_word_sense, get_trees
            if self.arg not in ctx.words:
                return False

            word=ctx.words[self.arg]
            sts = get_trees(word)
            return any([st.has_role(**roles) for st in sts])
        self.routines.append(fn)
        return self

    def run(self, key, ctx:Context):
        results = []
        for rt in self.routines:
            results.append(rt(key, ctx))
        return all(results)

    def __str__(self):
        return f"ins_{self.name()}({self.arg})"

