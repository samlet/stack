import requests
class ChineseCli(object):
    def parse(self, sents):
        """
        $ python -m sagas.zh.chinese_cli parse '我是一个学生'
        :param sents:
        :return:
        """
        from sagas.tool.misc import print_terms_zh
        data = {'lang': 'zh', "sents": sents}
        response = requests.post('http://localhost:8091/digest', json=data)
        if response.status_code == 200:
            result = response.json()
            print_terms_zh(data['sents'], result)

if __name__ == '__main__':
    import fire
    fire.Fire(ChineseCli)
