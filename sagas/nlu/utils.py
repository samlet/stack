import requests
from typing import Text, Any, Dict, List, Union, Optional
import re

from cachetools import cached
from sagas.conf.conf import cf

def alternate(sents):
    if '/' in sents:
        tokens = re.split(r"([.!?]) /", sents)
        if len(tokens)>1:
            sents=' '.join(tokens[0:2])
        else:
            sents=sents.replace(' / ', '/')
            words=[w.split('/')[0] for w in sents.split(' ')]
            sents=' '.join(words)
    return sents

def fix_sents(text:str, lang:str):
    text=alternate(text.strip())

    # 清除括号里的内容
    text = re.sub(r" ?\([^)]+\)", "", text)
    text=proc_lang_routines(text, lang)
    # 如果是中文和日文, 清除空格
    if lang in ('ja', 'zh'):
        text = text.replace(' ', '')
    elif lang=='es':
        text = text.replace('¿', '')
    return text

def join_text(r, lang):
    sent = ' '.join(r) if lang not in ('ja', 'zh') else ''.join(r)
    return sent

def fa_sents(sents):
    if '؟ ' in sents:
        return sents[:sents.index('؟ ') + 2]
    return sents

lang_routines={'fa': lambda s: fa_sents(s)}
def proc_lang_routines(s, l):
    if l in lang_routines:
        return lang_routines[l](s)
    return s

def word_values(word: Text, lang: Text):
    from sagas.nlu.transliterations import translits
    if '/' in word:
        text, lemma=word.split('/')
    else:
        text=lemma=word
    if translits.is_available_lang(lang):
        try:
            text_val=translits.translit(text, lang)
            return {'value':word, 'text':text_val,
                    'lemma':translits.translit(lemma, lang) if lemma.strip()!='' else text_val}
        except ValueError:
            print(f'*** value error: text: {text}, lemma: {lemma}')
    return {'value':word, 'text':text, 'lemma':lemma}

def get_possible_mean(specs):
    from collections import Counter
    if not specs:
        return ''
    elements = [s.split('.')[0] for s in specs]
    if elements:
        word_counts = Counter(elements)
        mean = word_counts.most_common(1)[0][0]
    else:
        mean = ''
    return mean

def get_word_sets(word:Text, lang:Text='en', pos:Text='*', first:bool=True) \
        -> Union[List[Dict[Text, Any]], Dict[Text, Any], None]:
    import requests
    from sagas.conf.conf import cf
    response = requests.post(f'{cf.ensure("words_servant")}/word_sets',
                             json={'word':word, 'lang':lang, 'pos':pos})
    if response.status_code == 200:
        sets= response.json()
        if sets:
            return sets[0] if first else sets
    return None

@cached(cache={})
def predicate(kind:Text, word:Text, lang:Text, pos:Text ) -> bool:
    # if '/' in kind or '/' in word:
    data = {'word': word, 'lang': lang, 'pos': pos,
            'kind': kind}
    response = requests.post(f'{cf.ensure("words_servant")}/predicate_chain',
                             json=data)
    # else:
    #     data = {'word': word, 'lang': lang, 'pos': pos,
    #             'kind': kind, 'only_first': only_first}
    #     response = requests.post(f'{cf.ensure("words_servant")}/predicate',
    #                              json=data)
    if response.status_code == 200:
        r = response.json()
        return r['result']
    return False

def check_chain(kind:Text, word:Text, pos:Text, lang:Text) -> bool:
    from sagas.nlu.synonyms import synonyms

    r = synonyms.match(word, lang)
    if r is None:
        return predicate(kind, word, lang, pos)
    return predicate(kind, r, 'en', pos)

