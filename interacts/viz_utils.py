import streamlit as st

@st.cache
def traviz(chunk, lang):
    import sagas
    v=lambda s: sagas.dia(lang, local_translit=True).ana(s)

    sents=chunk.split('\n')[1]
    return v(sents)

