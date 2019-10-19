import streamlit as st
from interacts.sl_utils import all_labels

def display_lang_selector():
    keys=list(all_labels.keys())
    idx_en=keys.index('English')
    language = st.sidebar.selectbox(
        'Which language do you choose?',
        list(keys),
        index=idx_en
    )

    cur_lang=all_labels[language]
    return cur_lang

