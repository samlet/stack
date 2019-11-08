from functools import singledispatch
import streamlit as st

from sagas.conf.conf import cf
from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.uni_remote import dep_parse
from sagas.nlu.uni_remote_viz import list_chunks, display_doc_deps
from sagas.nlu.utils import fix_sents

# viz('我要确认我预定的航班 。', 'zh')
tools=NluTools()

@singledispatch
def viz(sents, lang, verbose=False):
    raise NotImplementedError('Unsupported type')

@viz.register(str)
def _(sents, lang, verbose=False):
    from sagas.nlu.uni_remote_viz import viz_sample
    from sagas.conf.conf import cf
    # st.write(".. argument is of type ", type(arg))
    g = viz_sample(lang, sents, engine=cf.engine(lang))
    st.graphviz_chart(g)

def parse_deps(text, lang, translit=None):
    text = fix_sents(text, lang)
    engine = cf.engine(lang)
    # g = sentence_view(lang, text, engine=engine, translit_lang=lang, enable_contrast=True)
    doc_jsonify, resp = dep_parse(text, lang, engine, ['predicts'])
    if doc_jsonify is not None:
        list_chunks(doc_jsonify, resp, lang, enable_contrast=True)
        g = display_doc_deps(doc_jsonify, resp, translit_lang=lang)

        st.graphviz_chart(g)
        if translit is not None:
            st.text(f"♤ {translit}")

        words = [word.text for word in doc_jsonify.words]
        tools.contrast(text, lang, word_map=words)

exports={viz}

