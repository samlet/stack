import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.common import get_from_clip

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()
    return cur_lang

def main():
    lang=sidebar()
    st.subheader("Nlu Tools")

    text = st.text_area("Text to analyze", '')
    text=text.strip()
    if text!='':
        st.text(f'.. parse {text}')
        NluTools().clip_parse(lang, sents=text)

    if st.button('Parse copyboard text'):
        sents = get_from_clip()
        if sents.strip() != '':
            # text.text_area(sents)
            NluTools().clip_parse(lang, sents=sents)


if __name__ == '__main__':
    main()

