from json_utils import pretty_json

class ExtractorCli(object):
    def duckling(self, text, lang='en'):
        """
        $ python -m sagas.nlu.extractor_cli duckling 'tomorrow at eight' en
        $ python -m sagas.nlu.extractor_cli duckling "3 mins" en
        $ python -m sagas.nlu.extractor_cli duckling "last week" en
        $ python -m sagas.nlu.extractor_cli duckling "明天是九月九日" zh
        $ python -m sagas.nlu.extractor_cli duckling 'あしたは四月四日です。' ja
        $ python -m sagas.nlu.extractor_cli duckling '上周' zh
        $ python -m sagas.nlu.extractor_cli duckling "Maggio e giugno sono mesi dell'anno." it

        $ python -m sagas.nlu.extractor_cli duckling "fifty" en
        $ python -m sagas.nlu.extractor_cli duckling 'samlet@ymail.com' en  # "dim": "email"

        :param text:
        :param lang:
        :return:
        """
        from sagas.nlu.inspectors import query_duckling

        resp = query_duckling(text, lang)
        print(pretty_json(resp))
        print('-'*25)
        print([d['dim'] for d in resp['data']])

    def datetime(self, text, lang='en'):
        """
        $ python -m sagas.nlu.extractor_cli datetime 'tomorrow at eight' en
        $ python -m sagas.nlu.extractor_cli datetime 'two weeks ago' en
            .. search: [('two weeks ago', datetime.datetime(2019, 11, 29, 1, 57, 25, 466421))]
            .. parse: 2019-11-29 01:57:25.468518
        $ python -m sagas.nlu.extractor_cli datetime 'Jumat lalu' id
        $ python -m sagas.nlu.extractor_cli datetime '12 Mei 2008' id
            .. search: [('12 Mei 2008', datetime.datetime(2008, 5, 12, 0, 0))]
            .. parse: 2008-05-12 00:00:00
        $ python -m sagas.nlu.extractor_cli datetime 'Besok malam jam 8' id
            .. search: [('Besok', datetime.datetime(2019, 12, 1, 23, 22, 16, 689529)), ('jam 8', datetime.datetime(2019, 8, 30, 0, 0))]
            .. parse: None
        $ python -m sagas.nlu.extractor_cli datetime 'Minggu depan' id
            .. search: None
            .. parse: 2020-02-19 16:47:48.548957
        $ python -m sagas.nlu.extractor_cli datetime '三月开始去上学' zh
        $ python -m sagas.nlu.extractor_cli datetime '2008年12月に上海に行きたいです。' ja

        :param text:
        :param lang:
        :return:
        """
        from dateparser.search import search_dates
        from dateparser import parse
        # search_dates('Jumat lalu', languages=['id'])
        search_r=search_dates(text, languages=[lang])
        print(f".. search: {search_r}")
        # parse('12 Mei 2008', languages=['id'])
        parse_r=parse(text, languages=[lang])
        print(f".. parse: {parse_r}")

    def datetime_zh(self, text, rel=None):
        """
        $ python -m sagas.nlu.extractor_cli datetime_zh "周五下午7点到8点" "2017-07-19-00-00-00"

        :param text:
        :param rel:
        :return:
        """
        from sagas.zh.timenlp_procs import timenlp
        dt = timenlp.parse_dt(text, rel)
        for expr, val in dt:
            print(f"text:{expr}, date-time: {val}")

    def chunks(self, sents, lang, domain, path):
        """
        $ python -m sagas.nlu.extractor_cli chunks 'I like to eat sweet corn.' en verb 'xcomp/obj'
        $ python -m sagas.nlu.extractor_cli chunks 'A casa tem dezenove quartos.' pt verb 'obj'
            ☇ [('dezenove', 'num'), ('quartos', 'noun')]

        :param sents:
        :param lang:
        :param domain:
        :param path:
        :return:
        """
        from sagas.nlu.uni_chunks import get_chunk
        from sagas.nlu.ruleset_procs import list_words, cached_chunks
        from sagas.conf.conf import cf
        # get_chunk(f'verb_domains', 'xcomp/obj', lambda w: w.upos)
        # get_chunk(f'domain_domains', path, lambda w: w.upos)
        chunks = cached_chunks(sents, lang, cf.engine(lang))
        result=get_chunk(chunks, f'{domain}_domains', path, lambda w: (w.text, w.upos.lower()))
        print(result)

if __name__ == '__main__':
    import fire
    fire.Fire(ExtractorCli)

