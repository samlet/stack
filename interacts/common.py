import streamlit as st
from interacts.sl_utils import all_labels

def display_lang_selector():
    language = st.sidebar.selectbox(
        'Which language do you choose?',
         list(all_labels.keys()))

    cur_lang=all_labels[language]
    return cur_lang

