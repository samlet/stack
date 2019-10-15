import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels

def sidebar():
    cur_lang=display_lang_selector()

def main():
    sidebar()
    st.subheader("Intents")

if __name__ == '__main__':
    main()

