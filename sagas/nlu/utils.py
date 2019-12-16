import re

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

