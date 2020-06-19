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

def get_possible_mean(specs, algo='freq'):
    def count_word(elements:List[Text]):
        from collections import Counter
        word_counts = Counter(elements)
        mean = word_counts.most_common(1)[0][0]
        return mean

    def word_freq(elements:List[Text]):
        from wordfreq import zipf_frequency
        freqs=[(w, zipf_frequency(w, 'en')) for w in elements]
        return sorted(freqs, key=lambda x:-x[1])[0][0]

    fn={'count':count_word, 'freq':word_freq}
    if not specs:
        return ''
    elements = [s.split('.')[0] for s in specs]
    if elements:
        return fn[algo](elements)
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

def norm_pos(pos:Text):
    pos_cuts={'v':'verb', 'n':'noun', 'a':'adjective'}
    if pos is None:
        return None
    if len(pos)==1:
        return None if pos not in pos_cuts else pos_cuts[pos]
    elif pos.startswith('c_'):
        return pos[2:]
    return pos

def starts_with_in(w, *args):
    return any(w.startswith(arg) for arg in args)
def is_full_domain_path(path):
    return starts_with_in(path, 'verb:', 'aux:', 'subj:', 'predicts:')

def get_entities(seq, suffix=False):
    """Gets entities from sequence.
    Args:
        seq (list): sequence of labels.
    Returns:
        list: list of (chunk_type, chunk_start, chunk_end).
    Example:
        >>> from sagas.nlu.utils import get_entities
        >>> seq = ['B-PER', 'I-PER', 'O', 'B-LOC']
        >>> get_entities(seq)
        [('PER', 0, 1), ('LOC', 3, 3)]
    """
    # for nested list
    if any(isinstance(s, list) for s in seq):
        seq = [item for sublist in seq for item in sublist + ['O']]

    prev_tag = 'O'
    prev_type = ''
    begin_offset = 0
    chunks = []
    for i, chunk in enumerate(seq + ['O']):
        if suffix:
            tag = chunk[-1]
            type_ = chunk.split('-', maxsplit=1)[0]
        else:
            tag = chunk[0]
            type_ = chunk.split('-', maxsplit=1)[-1]

        if end_of_chunk(prev_tag, tag, prev_type, type_):
            chunks.append((prev_type, begin_offset, i - 1))
        if start_of_chunk(prev_tag, tag, prev_type, type_):
            begin_offset = i
        prev_tag = tag
        prev_type = type_

    return chunks


def end_of_chunk(prev_tag, tag, prev_type, type_):
    """Checks if a chunk ended between the previous and current word.
    Args:
        prev_tag: previous chunk tag.
        tag: current chunk tag.
        prev_type: previous type.
        type_: current type.
    Returns:
        chunk_end: boolean.
    """
    chunk_end = False

    if prev_tag == 'E': chunk_end = True
    if prev_tag == 'S': chunk_end = True

    if prev_tag == 'B' and tag == 'B': chunk_end = True
    if prev_tag == 'B' and tag == 'S': chunk_end = True
    if prev_tag == 'B' and tag == 'O': chunk_end = True
    if prev_tag == 'I' and tag == 'B': chunk_end = True
    if prev_tag == 'I' and tag == 'S': chunk_end = True
    if prev_tag == 'I' and tag == 'O': chunk_end = True

    if prev_tag != 'O' and prev_tag != '.' and prev_type != type_:
        chunk_end = True

    return chunk_end


def start_of_chunk(prev_tag, tag, prev_type, type_):
    """Checks if a chunk started between the previous and current word.
    Args:
        prev_tag: previous chunk tag.
        tag: current chunk tag.
        prev_type: previous type.
        type_: current type.
    Returns:
        chunk_start: boolean.
    """
    chunk_start = False

    if tag == 'B': chunk_start = True
    if tag == 'S': chunk_start = True

    if prev_tag == 'E' and tag == 'E': chunk_start = True
    if prev_tag == 'E' and tag == 'I': chunk_start = True
    if prev_tag == 'S' and tag == 'E': chunk_start = True
    if prev_tag == 'S' and tag == 'I': chunk_start = True
    if prev_tag == 'O' and tag == 'E': chunk_start = True
    if prev_tag == 'O' and tag == 'I': chunk_start = True

    if tag != 'O' and tag != '.' and prev_type != type_:
        chunk_start = True

    return chunk_start
