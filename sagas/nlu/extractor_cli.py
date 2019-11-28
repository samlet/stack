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
        $ python -m sagas.nlu.extractor_cli datetime 'Jumat lalu' id
        $ python -m sagas.nlu.extractor_cli datetime '12 Mei 2008' id
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

if __name__ == '__main__':
    import fire
    fire.Fire(ExtractorCli)

