import requests

from sagas.util.rest_common import query_data_by_url
from sagas.conf.conf import cf

def get_chains(word, lang, pos):
    response = requests.post(f'{cf.ensure("words_servant")}/get_chains',
                             json={'word': word, 'lang': lang, 'pos': pos})
    if response.status_code == 200:
        rs = response.json()
        return rs
    return []

def retrieve_word_info(path, word, lang, pos):
    """
    >>> from sagas.nlu.nlu_cli import retrieve_word_info
    >>> rs=retrieve_word_info('get_synsets', word, lang, pos)
    >>> retrieve_word_info('get_synsets', "いいです。/良い", 'ja', '*')

    :param path:
    :param word:
    :param lang:
    :param pos:
    :return:
    """
    response = requests.post(f'{cf.ensure("words_servant")}/%s'%path,
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

def scribes(dot):
    import io_utils
    import subprocess
    from subprocess import STDOUT
    io_utils.write_to_file('./out/sents.dot', dot.source, True)
    # $ graph-easy ./out/sents.dot --from=dot --as_ascii
    out_format = '--as_boxart'  # '--as_ascii'
    cmd_args = ['graph-easy', './out/sents.dot', '--from=dot', out_format]
    # r = subprocess.call(cmd_args)
    # print('done -', r)
    r = subprocess.check_output(cmd_args, stderr=STDOUT)
    result_text = r.decode('utf-8')
    # print(result_text)
    return result_text

def get_word_sets(word, lang='en', pos='*'):
    response = requests.post(f'{cf.ensure("words_servant")}/word_sets',
                             json={'word':word, 'lang':lang, 'pos':pos})
    # print(response.status_code, response.json())
    if response.status_code == 200:
        return {'result':'success','data': response.json()}
    return {'result':'fail'}

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
        return get_word_sets(word, lang, pos)

    def get_word_def(self, word, lang='en', pos='*'):
        """
        在终端上输出单词的定义和继承链.
        $ python -m sagas.nlu.nlu_cli get_word_def menina pt n
        $ python -m sagas.nlu.nlu_cli get_word_def cepillar es
        $ python -m sagas.nlu.nlu_cli get_word_def Krieg de
        $ def krieg de
        :param word:
        :param lang:
        :param pos:
        :return:
        """
        from termcolor import colored
        resp=get_word_sets(word, lang, pos)
        if resp['result']=='success':
            sets=resp['data']
            for s in sets:
                print("%s -> %s"%(colored(s['name'], 'green'), s['definition']))
                for exa in s['examples']:
                    print('\t', exa)
                domains=s['domains']
                print('\t', domains)
                # print('\t', s['lemmas'])
                for key, les in s['lemmas'].items():
                    if les:
                        # print('\t', '[%s] %s'%(key, ', '.join('_' if w is None else w for w in les)))
                        print('\t', '[%s] %s' % (key, ', '.join(les)))
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
        from pprint import pprint
        response = requests.post(f'{cf.ensure("words_servant")}/word_sets',
                                 json={'word': word, 'lang': lang, 'pos': pos})
        # print(response.status_code, response.json())
        if response.status_code == 200:
            rs = response.json()
            print('synsets:', ', '.join([r['name'].split('.')[0] for r in rs]))
            pprint(rs)
        else:
            print('fail')

    def print_synsets(self, word, lang, pos):
        """
        $ python -m sagas.nlu.nlu_cli print_synsets menina pt n
        :param word:
        :param lang:
        :param pos:
        :return:
        """
        # get_synsets
        rs=retrieve_word_info('get_synsets', word, lang, pos)
        print(rs)

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
            response = requests.post(f'{cf.ensure("words_servant")}/predicate',
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
                  {'word': 'колбаса', 'lang': 'ru', 'pos': 'n',
                   'kind': 'food/matter'},
                  ]
        for data in data_set:
            response = requests.post(f'{cf.ensure("words_servant")}/predicate_chain',
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
        from pprint import pprint

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

    def explore(self, word, lang='en', targets=None):
        """
        输出继承链以及在不同语言的词根表示
        $ python -m sagas.nlu.nlu_cli explore world en en,fr,ja,zh
        $ python -m sagas.nlu.nlu_cli explore dog en en,zh,de,ru
        $ expl kick
        :param word:
        :param lang:
        :param targets:
        :return:
        """
        import requests
        if targets is None:
            targets=['en', 'zh', 'ja', 'es','fr', 'de', 'ru']
        # data = {'word': 'world', 'lang': 'en', 'targets': ['en', 'fr', 'ja', 'zh']}
        data={'word':word, 'lang':lang, 'targets':targets}
        response = requests.post(f'{cf.ensure("words_servant")}/explore',
                                 json=data)
        if response.status_code == 200:
            resp = response.json()
            print_explore(resp)
        else:
            print('fail.')

    def ascii_viz(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.nlu.nlu_cli ascii_viz 'what time is it ?' en
        $ ascviz '我是一个学生' zh

        :param sents:
        :param lang:
        :return:
        """
        from sagas.nlu.uni_remote_viz import viz_sample
        # sents = 'what time is it ?'
        dot = viz_sample(lang, sents, engine=engine,
                         translit_lang=lang if lang in ('ja', 'ko','zh', 'fa', 'ar', 'he') else None)
        return scribes(dot)

    def tokens(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.nlu_cli tokens 'what time is it ?' en
        $ python -m sagas.nlu.nlu_cli tokens "在终端上输出单词的定义和继承链" zh
        $ python -m sagas.nlu.nlu_cli tokens "望遠鏡で泳いでいる少女を見た。" ja

        :param sents:
        :param lang:
        :return:
        """
        from pprint import pprint
        r=query_data_by_url('multilang', 'tokens', {'lang': lang, 'sents': sents})
        pprint(r)

    def predicate(self, kind, word, lang, pos):
        """
        $ python -m sagas.nlu.nlu_cli predicate 'weather/phenomenon' weather en n

        :param kind:
        :param word:
        :param lang:
        :param pos:
        :return:
        """
        from sagas.nlu.inspector_wordnet import predicate

        print(f"{word} is category {kind}: {predicate(kind, word, lang, pos)}")

if __name__ == '__main__':
    import fire
    fire.Fire(NluCli)

