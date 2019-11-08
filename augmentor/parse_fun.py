from functools import singledispatch
from decimal import Decimal
import streamlit as st
from interacts.sl_utils import fix_data
from sagas.nlu.nlu_tools import NluTools
from sagas.tool.misc import get_verb_domains

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

@singledispatch
def domains(arg, lang=None):
    raise NotImplementedError('Unsupported type')

dataset=[{'lang': 'de', "sents": 'Die Aufnahmen begannen im November.', 'engine':'corenlp'},
         {'lang': 'ko', "sents": '언어를 배우는 것은 흥미로워요.', 'engine':'corenlp'},
         {'lang': 'it', "sents": 'Gli piace ascoltare la musica.'},
         {'lang': 'ja', "sents": 'なぜ あなたは 時間どおりに 来られなかったの です か ？'},
         ]
# data = {'lang': 'de', "sents": 'Die Aufnahmen begannen im November.', 'engine':'corenlp'}

@domains.register(str)
def _(arg, lang=None):
    st.write(".. argument is of type ", type(arg))
    if lang is None:
        for data in dataset:
            if st.button(f"{data['lang']} ☑ {data['sents']}"):
                _ = get_verb_domains(fix_data(data))
    else:
        data={'lang':lang, 'sents':arg}
        _ = get_verb_domains(fix_data(data))

exports={parse, domains}


