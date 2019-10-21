stuffs={
    'en': 'I don’t like mushrooms.',
    'ja': '私は ホテルが 必要 です 。',
    'ko': '저는 양파를 안 좋아해요.',
    'fa': '‫او با کامپیوتر کار می‌کند.‬',
    'zh': '我 要 确认 我预定的 航班 。',
}

def get_stuff(lang):
    if lang in stuffs:
        return stuffs[lang]
    return ''

def get_parse_skel(lang):
    text=get_stuff(lang)
    if text!='':
        return f"parse('{text}', '{lang}')"
    return ''



