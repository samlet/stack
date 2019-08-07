import requests
from pprint import pprint

def get_chains(word, lang, pos):
    response = requests.post('http://localhost:8093/get_chains',
                             json={'word': word, 'lang': lang, 'pos': pos})
    if response.status_code == 200:
        rs = response.json()
        return rs
    return []

def print_explore(rs):
    for c in rs:
        print('%d. %s'%(c['index'], c['name']))
        for level in c['hyper']:
            print('\t%s: %s'%(level['name'], level['definition']))
            for rec in level['records']:
                print('\t\t[%s] %s'%(rec['lang'], ', '.join(rec['lemmas'])))


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

    def get_word_def(self, word, lang='en', pos='*'):
        """
        $ python -m sagas.nlu.nlu_cli get_word_def menina pt n
        $ python -m sagas.nlu.nlu_cli get_word_def cepillar es
        :param word:
        :param lang:
        :param pos:
        :return:
        """
        from termcolor import colored
        resp=self.get_word_sets(word, lang, pos)
        if resp['result']=='success':
            sets=resp['data']
            for s in sets:
                print("%s -> %s"%(colored(s['name'], 'green'), s['definition']))
                for exa in s['examples']:
                    print('\t', exa)
                domains=s['domains']
                print('\t', domains)
        print(colored('✁ --------------------------', 'red'))
        self.get_chains(word, lang, pos)

    def print_defs(self, word, lang, pos):
        """
        $ python -m sagas.nlu.nlu_cli print_defs menina pt n
        :param word:
        :param lang:
        :param pos:
        :return:
        """
        response = requests.post('http://localhost:8093/word_sets',
                                 json={'word': word, 'lang': lang, 'pos': pos})
        # print(response.status_code, response.json())
        if response.status_code == 200:
            rs = response.json()
            print('synsets:', ', '.join([r['name'].split('.')[0] for r in rs]))
            pprint(rs)
        else:
            print('fail')

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

    def get_chains(self, word, lang, pos, simple=True):
        """
        $ python -m sagas.nlu.nlu_cli get_chains menina pt n
        :param word:
        :param lang:
        :param pos:
        :return:
        """
        from termcolor import colored

        resp=get_chains(word, lang, pos)
        if len(resp)>0:
            if not simple:
                pprint(resp)
            else:
                for chain in resp:
                    print("%s %s: %s"%(colored(chain['offset'], 'green'),
                                       colored(chain['name'], 'red'),
                                       ', '.join(chain['chain'])))
        else:
            print('none.')

    def explore(self, word, lang, targets):
        """
        $ python -m sagas.nlu.nlu_cli explore world en en,fr,ja,zh
        :param word:
        :param lang:
        :param targets:
        :return:
        """
        import requests
        # data = {'word': 'world', 'lang': 'en', 'targets': ['en', 'fr', 'ja', 'zh']}
        data={'word':word, 'lang':lang, 'targets':targets}
        response = requests.post('http://localhost:8093/explore',
                                 json=data)
        if response.status_code == 200:
            resp = response.json()
            print_explore(resp)
        else:
            print('fail.')

if __name__ == '__main__':
    import fire
    fire.Fire(NluCli)
