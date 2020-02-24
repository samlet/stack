import re
import pyknp
from cachetools import cached

# KNP preparing:
# option (str) – KNP解析オプション (詳細解析結果を出力する-tabは必須。
# 省略・照応解析を行う -anaphora, 格解析を行わず構文解析のみを行う -dpnd など)

knp_ner = pyknp.KNP(option="-tab -dpnd", jumanpp=False)

@cached(cache={})
def ner(src_text: str):
    rs=[]
    result = knp_ner.parse(src_text)  # tagging

    for tag in result.tag_list():
        if "NE:" in tag.fstring:  # if fstring has NE phrase
            span=result.get_tag_span(tag.tag_id)
            # extract NE phrase
            search_r=re.search("<NE:(.*):(.*)>", tag.fstring)

            tagged_ne_phrase =search_r.group(0)
            ne_phrase=search_r.group(2)
            ent=search_r.group(1)

            rs.append({'text': ne_phrase,
                       'start': span[0],
                       'end': span[1],
                       'entity': ent})

    return rs

