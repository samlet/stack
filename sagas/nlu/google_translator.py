from typing import Text, Any, Dict, List, Union
import random

import requests
import json
from bs4 import BeautifulSoup
## $ pip install PyExecJS
import execjs # 执行js脚本
import logging

logger = logging.getLogger(__name__)

class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
      };      
      function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
      } 
     """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


js = Py4Js()

def buildUrl(text,tk, source='auto', target='zh-CN'):
    baseUrl = 'https://translate.google.cn/translate_a/single'
    baseUrl += '?client=t&'

    # baseUrl+='s1=auto&'
    baseUrl += 'sl=%s&' % source
    # baseUrl+='t1=zh-CN&'
    baseUrl += 'tl=%s&' % target
    # baseUrl+='h1=zh-CN&'
    baseUrl += 'hl=en&'

    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    baseUrl += 'ie=UTF-8&'
    baseUrl += 'oe=UTF-8&'
    baseUrl += 'otf=1&'
    baseUrl += 'pc=1&'
    baseUrl += 'ssel=0&'
    baseUrl += 'tsel=0&'
    baseUrl += 'kc=2&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'q=' + text

    return baseUrl

def join_sentence(r):
    if len(r)==0:
        return ''
    if r[0] is None:
        return ''
    
    rs=[]
    for sent in r[0]:
        if sent[0] is not None:
            # print('%s ✔ %s' % (sent[0], sent[1]))
            rs.append(sent[0])
    return ' '.join(rs)

def translations_df(trans):
    import sagas
    # fill with default field names
    size = len(trans[0][2][0])
    # print('size', size)
    listOfStrings = ['ext_' + str(i) for i in range(size)]
    if size==2:
        listOfStrings[0:2] = ['word', 'translations']
    else:
        listOfStrings[0:4] = ['word', 'translations', 'c', 'freq']

    return sagas.to_df(trans[0][2], listOfStrings)

def display_translations(trans):
    from tabulate import tabulate
    print(tabulate(translations_df(trans), headers='keys', tablefmt='psql'))

class TransTracker(object):
    def __init__(self, *obs):
        self.pronounce=[]
        # word translations as a pandas dataframe
        self.translations=None
        self.obs = list(obs)

    def add_observer(self, observer):
        if observer not in self.obs:
            self.obs.append(observer)

    def delete_observer(self, observer):
        self.obs.remove(observer)

    def notify_observers(self, meta, r=None):
        localArray = self.obs[:]
        # Updating is not required to be synchronized:
        for observer in localArray:
            observer.update(meta, r)

    def observer(self, type_of):
        return next(ob for ob in self.obs if type(ob)==type_of)

class WordsObserver(object):
    def __init__(self):
        self.word_trans_df=None
    def update(self, meta, r):
        if r[1]:
            self.word_trans_df=translations_df(r[1])

    @property
    def candidates(self) -> List[Text]:
        if self.word_trans_df is not None:
            candidates = [w for w in self.word_trans_df['word']]
        else:
            candidates = []
        return candidates

def with_words():
    """
    >>> from sagas.nlu.google_translator import translate, with_words, WordsObserver
    >>> r,t=translate('गतिविधि', source='hi', target='en', options={'get_pronounce'}, tracker=with_words())
    >>> print(r)
    >>> t.observer(WordsObserver).word_trans_df

    :return:
    """
    from sagas.nlu.trans_cacher import cacher
    return TransTracker(cacher, WordsObserver())

def process_result(meta, r, trans_verbose, options, tracker:TransTracker):
    # import sagas
    tracker.notify_observers(meta, r)
    if trans_verbose:
        print('❶ total result', len(r))
        for rl in r:
            print("♥", rl)
        print('--------------------------')
        # print(r[0])
        print('❷ total sents', len(r[0]))
        for sent in r[0]:
            print('❣', sent)
        if r[1] is not None:
            print('② translations for word')
            # print(r[1])
            display_translations(r[1])

        print('--------------------------')
        print('❸ tidy lines')
        for sent in r[0]:
            if sent[0] is not None:
                print('%s ✔ %s'%(sent[0], sent[1]))
            else:
                # pronounces
                for pr in sent:
                    if pr is not None:
                        print('ﺴ', pr)
        print('✁-------------------------')

    if 'get_pronounce' in options:
        for sent in r[0]:
            if sent[0] is None:
                for pr in sent:
                    if pr is not None:
                        # print('ﺴ', pr)
                        tracker.pronounce.append('❣ '+pr)
    if 'get_translations' in options:
        if r[1] is not None:
            trans=r[1]
            # tracker.translations=sagas.to_df(trans[0][2], ['word', 'translations', 'c', 'freq'])
            tracker.translations =translations_df(trans)


def translate(text, source='auto', target='zh-CN', trans_verbose=False, options=None, tracker=None):
    import sagas.conf.conf as conf
    from sagas.nlu.trans_cacher import cacher
    import time

    if options is None:
        options = {}

    # tracker=TransTracker()
    meta = {'text': text, 'source': source, 'target': target}

    if tracker is None:
        if conf.cf.is_enabled('trans_cache'):
            tracker = TransTracker()
            tracker.add_observer(cacher)
        else:
            tracker = TransTracker()

    if 'disable_cache' not in options:
        # try to get from cacher
        r = cacher.retrieve(meta)
        if r:
            cnt = r['content']
            res = join_sentence(cnt)
            process_result(meta, cnt, trans_verbose, options, tracker)
            logger.debug(f'get {text} from cacher')
            return res, tracker

    header = {
        'authority': 'translate.google.cn',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
    }
    url = buildUrl(text, js.getTk(text), source, target)
    res = ''
    try:
        time.sleep(random.uniform(0.05, 0.20))
        r = requests.get(url, headers=header, timeout=1.5)
        result = json.loads(r.text)
        # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
        # if result[7]!=None:
        if result[7] is not None and 'disable_correct' not in options:
            try:
                correctText = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                print(correctText)
                correctUrl = buildUrl(correctText, js.getTk(correctText), source, target)
                correctR = requests.get(correctUrl)
                newResult = json.loads(correctR.text)
                # res=newResult[0][0][0]
                res = join_sentence(newResult)

                process_result(meta, newResult, trans_verbose, options, tracker)
            except Exception as e:
                # print('translate error: ', e, f", in process text {text}")
                # res=result[0][0][0]
                res = join_sentence(result)
                process_result(meta, result, trans_verbose, options, tracker)
        else:
            process_result(meta, result, trans_verbose, options, tracker)
            # res=result[0][0][0]
            res = join_sentence(result)
    except Exception as e:
        res = ''
        logger.error("translate fail: " + text)
        logger.error("error message: %s", e)
    finally:
        return res, tracker


def marks(t, ips_idx):
    if len(t.pronounce)>0:
        return ', '+t.pronounce[ips_idx][1:]
    return ''

def get_word_map(source, target, text, ips_idx=0, words=None, local_translit=False):
    """
    Example 1:
    from sagas.nlu.corenlp_helper import CoreNlp, CoreNlpViz, get_nlp
    ana=lambda sents: CoreNlpViz().analyse(sents, get_nlp('hi'), get_word_map('hi','en', sents)[0])
    ana('मेरे पास दो रेफ्रिजरेटर हैं')

    Example 2:
    get_word_map('hi','en', 'मेरे पास दो रेफ्रिजरेटर')[0]

    :param source:
    :param target:
    :param text:
    :param ips_idx:
    :return:
    """
    from sagas.nlu.transliterations import translits

    rs = {}
    verbose = False
    options = {'get_pronounce', 'disable_correct'}
    if words is None:
        words=text.split(' ')

    trans_table=[]
    for sent in words:
        res, t = translate(sent, source=source, target=target,
                           trans_verbose=verbose, options=options)
        # print(res, sent, t[ips_idx])
        if local_translit and translits.is_available_lang(source):
            trans=', '+translits.translit(sent, source)
        else:
            trans=marks(t, ips_idx)
        rs[sent] = '%s\n(%s%s)' % (sent, res, trans)
        res_r=f"({res})" if res!='' and res not in ('(', ')', '[', ']', '/') else ''
        trans_table.append(f"{trans[2:]}{res_r}")
    return rs, trans_table

def trans_multi(sent, source, targets):
    """
    from sagas.nlu.google_translator import trans_multi
    trans_multi('Jopará é unha forma falada da lingua guaraní que.', 'gl', ['en', 'es'])
    :param sent:
    :param source:
    :param targets:
    :return:
    """
    options = {'get_pronounce', 'disable_correct'}
    verbose=False
    rs=[]
    for target in targets:
        res, _ = translate(sent, source=source, target=target,
            trans_verbose=verbose, options=options)
        rs.append(res)
    return rs




