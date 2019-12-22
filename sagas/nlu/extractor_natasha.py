icon_maps_text="""AddressExtractor ↘
DatesExtractor ♯
LocationExtractor ♮
MoneyExtractor ￥
MoneyRangeExtractor ∈
MoneyRateExtractor ￠
SimpleNamesExtractor ♡
OrganisationExtractor ✡
PersonExtractor ☃""".split('\n')
icon_maps={}
for el in icon_maps_text:
    parts=el.split(' ')
    icon_maps[parts[0]]=parts[1]

class NatashaExtractor(object):
    def __init__(self):
        from natasha import (
            NamesExtractor,
            SimpleNamesExtractor,
            DatesExtractor,
            MoneyExtractor,
            MoneyRateExtractor,
            MoneyRangeExtractor,
            LocationExtractor,
            AddressExtractor,
            OrganisationExtractor,
            PersonExtractor
        )

        addr_ex = AddressExtractor()
        date_ex = DatesExtractor()
        loc_ex = LocationExtractor()
        money_ex = MoneyExtractor()
        money_range_ex = MoneyRangeExtractor()
        money_rate_ex = MoneyRateExtractor()
        name_ex = SimpleNamesExtractor()
        org_ex = OrganisationExtractor()
        person_ex = PersonExtractor()
        # extractors=[addr_ex, date_ex, loc_ex, money_ex, money_range_ex, money_rate_ex,
        #            name_ex, org_ex, person_ex]
        self.extractors = [addr_ex, date_ex, loc_ex, money_ex, money_range_ex, money_rate_ex,
                      org_ex, person_ex]

    def all_extractor_names(self):
        for extractor in self.extractors:
            print(type(extractor).__name__)

    def extract_segs(self, text):
        result = []
        for extractor in self.extractors:
            matches = extractor(text)
            if len(matches) > 0:
                ex_name = type(extractor).__name__
                icon = icon_maps[ex_name]
                for match in matches:
                    start, stop = match.span
                    result.append(icon + text[start:stop])
        return result

    def extract(self, text):
        """
        $ python -m sagas.nlu.extractor_natasha extract 'Россия, Вологодская обл. г. Череповец, пр.Победы 93 б'
        :param text:
        :return:
        """
        result = []
        for extractor in self.extractors:
            matches = extractor(text)
            if len(matches) > 0:
                ex_name = type(extractor).__name__.replace('Extractor', '').lower()
                for match in matches:
                    start, stop = match.span
                    result.append({'text':text[start:stop],
                                   'start':start,
                                   'end':stop,
                                   'entity':ex_name})
        return result

    def extract_df(self, text):
        """
        extract_df('Россия, Вологодская обл. г. Череповец, пр.Победы 93 б')
        :param text:
        :return:
        """
        import sagas
        result = []
        for extractor in self.extractors:
            matches = extractor(text)
            if len(matches) > 0:
                ex_name = type(extractor).__name__.replace('Extractor', '').lower()
                for match in matches:
                    start, stop = match.span
                    result.append((text[start:stop], start, stop,
                                   ex_name, match.fact))
        return sagas.to_df(result, ['word', 'start', 'stop', 'extractor', 'fact'])

    def to_df(self, text):
        """
        $ python -m sagas.nlu.extractor_natasha to_df 'Россия, Вологодская обл. г. Череповец, пр.Победы 93 б'
        :param text:
        :return:
        """
        print("(%s)"%'; '.join(self.extract_segs(text)))
        print(self.extract_df(text))

ru_natasha=NatashaExtractor()

if __name__ == '__main__':
    import fire
    fire.Fire(NatashaExtractor)

