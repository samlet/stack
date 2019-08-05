import requests

class NluCli(object):
    def get_word_sets(self, word, lang='en', pos='*'):
        """
        $ python -m sagas.nlu.nlu_cli get_word_sets boat
        $ python -m sagas.nlu.nlu_cli get_word_sets menina pt
        $ python -m sagas.nlu.nlu_cli get_word_sets menina pt n
        $ python -m sagas.nlu.nlu_cli get_word_sets fly en n
        $ python -m sagas.nlu.nlu_cli get_word_sets fly en v
        $ python -m sagas.nlu.nlu_cli get_word_sets xyz en n
            result: success
            data:   []

        :param word:
        :param lang:
        :return:
        """
        response = requests.post('http://localhost:8093/word_sets',
                                 json={'word':word, 'lang':lang, 'pos':pos})
        # print(response.status_code, response.json())
        if response.status_code == 200:
            return {'result':'success','data': response.json()}
        return {'result':'fail'}

    def testings(self):
        """
        $ python -m sagas.nlu.nlu_cli testings
        :return:
        """
        data_set=[{'word': 'wolf', 'lang': 'en', 'pos': 'n',
                   'kind':'animal', 'only_first':True},
                  {'word': 'wolf', 'lang': 'en', 'pos': 'n',
                   'kind': 'wolf', 'only_first': True},
                  {'word': 'wolf', 'lang': 'en', 'pos': 'n',
                   'kind': 'clothing', 'only_first': True},
                  {'word': 'sweater', 'lang': 'en', 'pos': 'n',
                   'kind': 'clothing', 'only_first': True},
                  {'word': 'yellow', 'lang': 'en', 'pos': 'n',
                   'kind': 'color', 'only_first': True},
                  {'word': 'amarelo', 'lang': 'pt', 'pos': 'n',
                   'kind': 'color', 'only_first': True},
                  ]
        for data in data_set:
            response = requests.post('http://localhost:8093/predicate',
                                     json=data)
            if response.status_code == 200:
                print('(%s) %s is %s'%(data['lang'], data['word'], data['kind']),
                      {'result': 'success', 'data': response.json()})
            else:
                print({'result': 'fail'})

    def testing_chains(self):
        """
        $ python -m sagas.nlu.nlu_cli testing_chains
        :return:
        """
        data_set=[{'word': 'wolf', 'lang': 'en', 'pos': 'n',
                   'kind':'animal/mammal'},
                  {'word': 'amarelo', 'lang': 'pt', 'pos': 'n',
                   'kind': 'color'},
                  ]
        for data in data_set:
            response = requests.post('http://localhost:8093/predicate_chain',
                                     json=data)
            if response.status_code == 200:
                resp=response.json()
                print('%s (%s) %s is %s'%('✔' if resp['result'] else '✘',
                    data['lang'], data['word'], data['kind']), resp)
            else:
                print('fail')

if __name__ == '__main__':
    import fire
    fire.Fire(NluCli)
