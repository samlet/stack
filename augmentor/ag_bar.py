import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

from augmentor.add_fun import add

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()
    use_textarea=st.sidebar.checkbox('Use textarea')
    return cur_lang, use_textarea

def main():
    cur_lang, use_textarea=sidebar()
    st.subheader("Augmentor Bar")
    if use_textarea:
        cmd = st.text_area("Command to execute", '')
    else:
        cmd=st.text_input("Command to execute", '')
    if cmd != '':
        # st.write(cmd)
        exec(cmd)

if __name__ == '__main__':
    main()

