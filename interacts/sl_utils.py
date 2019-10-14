import re

all_labels = {"Dutch":'nl', "Persian":'fa', "Japanese":'ja',
              "Korea":'ko', "Afrikaans":'af', "Russian":'ru',
              "Italian":'it', "Turkish":'tr', 'Finnish':'fi',
              'Estonian':'et',
              "Arabic":'ar'}

def fix_sents(text, lang):
    text = re.sub(r" ?\([^)]+\)", "", text)
    if lang in ('ja', 'zh'):
        text = text.replace(' ', '')
    return text
