from sagas.nlu.inspector_common import Inspector, Context


class CompExtractInspector(Inspector):
    """
    提取指定成分:
    >>> pat(3, name='extract_day').cop(behaveof('day', 'n'),
                                              flat=kindof('feast_day/day', 'n'),
                                              nsubj=extract('plain+date_search+date_parse')),
    """
    def __init__(self, comp_as='plain', pickup=None):
        self.comp_as=comp_as.split('+')
        self.pickup=pickup

    def name(self):
        return "extract_comps"

    def run(self, key, ctx:Context):
        key=self.pickup or key
        def ex_date_search(cnt, comp):
            from dateparser.search import search_dates
            search_r = search_dates(cnt, languages=[ctx.lang])
            if search_r is not None:
                ctx.add_result(self.name(), comp, key, [str(r) for r in search_r])
        def ex_date_parse(cnt, comp):
            from dateparser import parse
            parse_r = parse(cnt, languages=[ctx.lang])
            if parse_r is not None:
                ctx.add_result(self.name(), comp, key, str(parse_r))
        def ex_plain(cnt, comp):
            ctx.add_result(self.name(), comp, key, cnt)

        ex_map={'date_search': ex_date_search,
                'date_parse': ex_date_parse,
                'plain': ex_plain,
                }
        for comp in self.comp_as:
            for cnt in ctx.chunk_pieces(key):
                ex=ex_map[comp]
                ex(cnt, comp)

        return True  # 只负责提取, 并不参与判定, 所以始终返回True

    def __str__(self):
        return f"ins_{self.name()}({self.comp_as})"

extract=lambda c='plain': CompExtractInspector(c)
extract_dt=lambda c='plain+date_search+date_parse': CompExtractInspector(c)
extract_c=lambda p: CompExtractInspector('plain', p)
