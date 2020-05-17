import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

def main():
    sidebar()
    st.subheader("Application")

if __name__ == '__main__':
    main()

