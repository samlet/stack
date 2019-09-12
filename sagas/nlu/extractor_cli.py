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

if __name__ == '__main__':
    import fire
    fire.Fire(ExtractorCli)

