from typing import Text, Any, Dict, List, Union, Set, Optional

import logging
import time
import random
from sagas.conf.conf import cf
from sagas.nlu.translator_intf import join_sentence, TransTracker
import sagas.tracker_fn as tc
from sagas.nlu.utils import norm_pos

logger = logging.getLogger(__name__)

def translations_df(trans, idx=0):
    import sagas
    # fill with default field names
    size = len(trans[idx][2][0])
    # print('size', size)
    listOfStrings = ['ext_' + str(i) for i in range(size)]
    if size==2:
        listOfStrings[0:2] = ['word', 'translations']
    else:
        listOfStrings[0:4] = ['word', 'translations', 'c', 'freq']

    return sagas.to_df(trans[idx][2], listOfStrings)

def display_translations(trans):
    from tabulate import tabulate
    for idx, el in enumerate(trans):
        tc.emp('cyan', '⊕', el[0])
        tc.emp('yellow', tabulate(translations_df(trans, idx), headers='keys', tablefmt='psql'))

class WordsObserver(object):

    def __init__(self):
        self.word_trans_df=None # default
        self.trans_dfs={} # key is pos: noun, verb, adjective, adverb, conjunction

    def fill_trans_map(self, trans):
        for idx, el in enumerate(trans):
            self.trans_dfs[el[0]]=translations_df(trans, idx)

    def update(self, meta, r):
        if r[1]:
            self.word_trans_df=translations_df(r[1])
            self.fill_trans_map(r[1])

    def get_candidates(self, pos:Optional[Text]=None) -> List[Text]:
        pos = norm_pos(pos)
        if pos is None:
            if self.word_trans_df is not None:
                return [w for w in self.word_trans_df['word']]
        else:
            if pos in self.trans_dfs:
                df=self.trans_dfs[pos]
                return [w for w in df['word']]
        return []

    def get_axis(self, default:Text, pos:Optional[Text]=None):
        candidates=self.get_candidates(pos)
        if candidates and candidates[0]!=default:
            return f"{candidates[0]}/{default}"
        return default

    candidates = property(get_candidates)


def with_words():
    """
    >>> from sagas.nlu.translator import translate, with_words, WordsObserver
    >>> r,t=translate('गतिविधि', source='hi', target='en', options={'get_pronounce'}, tracker=with_words())
    >>> print(r)
    >>> t.observer(WordsObserver).word_trans_df

    :return:
    """
    from sagas.nlu.trans_cacher import cacher
    return TransTracker(cacher, WordsObserver())

def process_result(meta:Dict[Text, Text], r, trans_verbose,
                   options:Set[Text], tracker:TransTracker):
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


def translate(text, source:Text='auto', target:Text='zh-CN',
              trans_verbose:bool=False, options:Set[Text]=None,
              tracker:TransTracker=None) -> (Text, TransTracker):
    from sagas.nlu.trans_cacher import cacher

    if options is None:
        options = {}

    # tracker=TransTracker()
    meta = {'text': text, 'source': source, 'target': target}

    if tracker is None:
        if cf.is_enabled('trans_cache'):
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

    def impl():
        from sagas.nlu.translator_impl import TranslatorImpl
        time.sleep(random.uniform(0.05, 0.20))
        trans_text=TranslatorImpl().execute(text, source, target, trans_verbose,
                                 options, tracker, process_result=process_result)
        return trans_text

    def impl2():
        from sagas.nlu.translator2_impl import translator_impl
        time.sleep(random.uniform(0.05, 0.20))
        translator_impl.update_TKK()  # update kk value
        time.sleep(random.uniform(0.05, 0.20))
        return translator_impl.execute(text, source, target, trans_verbose,
                                 options, tracker, process_result=process_result)

    trans_fn={'impl': impl, 'impl2': impl2}
    trans_text=trans_fn[cf.ensure('translator_impl')]()
    return trans_text, tracker


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




