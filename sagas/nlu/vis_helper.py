from natasha.markup import format_markup_css
class Matches(object):
    __attributes__ = ['text', 'matches']

    def __init__(self, text, matches, use_dict=False):
        self.text = text
        # self.matches = sorted(matches, key=lambda _: _.span)
        # self.matches = sorted(r.entities, key=lambda _: _.start)
        self.matches = matches
        self.use_dict=use_dict

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
        spans = [(_.start,_.end) for _ in self.matches]
        return ''.join(format_markup_css(self.text, spans))

