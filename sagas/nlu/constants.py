viz_translit_langs={'ja', 'ko','zh', 'fa', 'ar', 'he', 'ug', 'hi'}
contrast_translit_langs={'fa', 'ur', 'he', 'ug', 'hi'}
non_spaces=['ja', 'zh']
def delim(lang):
    return '' if lang in non_spaces else ' '

