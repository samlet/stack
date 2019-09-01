import opencc
from pypinyin import lazy_pinyin

s2t=lambda x: opencc.convert(x, config='s2twp.json')
t2s=lambda x: opencc.convert(x, config='tw2sp.json')
pinyin=lambda x: ' '.join(lazy_pinyin(x))


