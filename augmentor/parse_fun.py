from functools import singledispatch
from decimal import Decimal
import streamlit as st

from sagas.nlu.nlu_tools import NluTools


@singledispatch
def parse(text, lang, verbose=False):
    """
    >>> parse('저는 양파를 안 좋아해요.', 'ko')
    :param text:
    :param lang:
    :param verbose:
    :return:
    """
    if verbose:
        st.write("Let me just say,")
    st.write(text)

@parse.register(str)
def _(text, lang, verbose=False):
    st.text(f'.. parse {text}')
    NluTools().clip_parse(lang, sents=text)


@parse.register(list)
def _(texts, lang, verbose=False):
    """
    >>> parse(['我 要 确认 我预定的 航班 。', '我 要 取消 预定的 航班 。'], 'zh')
    :param texts:
    :param lang:
    :param verbose:
    :return:
    """
    for text in texts:
        st.markdown(f'.. **parse** `{text}`')
        NluTools().clip_parse(lang, sents=text)

exports={parse}


