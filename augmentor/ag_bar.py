import streamlit as st

from augmentor.corpus_tool import get_parse_skel
from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
import shlex

# functions
from augmentor.add_fun import add
from augmentor.test_fun import fun
from augmentor.parse_fun import parse

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()
    use_textarea=st.sidebar.checkbox('Use textarea')
    exec_as_function=st.sidebar.checkbox('Execute as function', value=True)
    return cur_lang, use_textarea, exec_as_function

def exec_func(cmd, exec_as_function):
    if exec_as_function:
        exec(cmd)
    else:
        fc = shlex.split(cmd)
        eval(fc[0])(*fc[1:])

def main():
    cur_lang, use_textarea, exec_as_function=sidebar()
    st.subheader("Augmentor Bar")
    if use_textarea:
        cmd = st.text_area("Command to execute", get_parse_skel(cur_lang))
    else:
        cmd=st.text_input("Command to execute", get_parse_skel(cur_lang))
    if cmd != '':
        # st.write(cmd)
        exec_func(cmd, exec_as_function)

if __name__ == '__main__':
    main()

