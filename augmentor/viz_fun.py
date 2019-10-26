from functools import singledispatch
import streamlit as st

# viz('我要确认我预定的航班 。', 'zh')

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

exports={viz}

