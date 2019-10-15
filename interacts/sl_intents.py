import streamlit as st

from interacts.sl_utils import all_labels

language = st.sidebar.selectbox(
    'Which language do you choose?',
     list(all_labels.keys()))

cur_lang=all_labels[language]

st.subheader("Intents")

