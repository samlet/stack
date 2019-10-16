def fix_sents(text:str, lang:str):
    import re
    text = re.sub(r" ?\([^)]+\)", "", text)
    if lang in ('ja', 'zh'):
        text = text.replace(' ', '')
    return text

def join_text(r, lang):
    sent = ' '.join(r) if lang not in ('ja', 'zh') else ''.join(r)
    return sent

