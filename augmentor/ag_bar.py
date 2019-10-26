import streamlit as st

from augmentor.corpus_tool import get_parse_skel
from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
import shlex

from datetime import datetime
from dateutil.parser import parse as dt

# functions
from augmentor.add_fun import add
from augmentor.test_fun import fun
from augmentor.parse_fun import parse
from augmentor.entity_fun import ent, browse
from augmentor.chart_fun import chart
from augmentor.maps_fun import maps
from augmentor.viz_fun import viz
from augmentor.corpus_fun import corpus, corpus_audio
from augmentor.product_fun import product

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()
    use_textarea=st.sidebar.checkbox('Use textarea')
    exec_as_function=st.sidebar.checkbox('Execute as function', value=True)
    return cur_lang, use_textarea, exec_as_function

def list_fn_files():
    import glob
    import ntpath
    for f in glob.glob(f'./*_fun.py'):
        fname=ntpath.basename(f).replace('.py', '')
        st.markdown(f"`{fname}`")

internal_fn={'fn_list':list_fn_files}

def exec_func(cmd:str, exec_as_function):

    if cmd.startswith('!'):
        inf=cmd[1:]
        if inf in internal_fn:
            internal_fn[inf]()
        return

    if exec_as_function:
        exec(cmd)
    else:
        fc = shlex.split(cmd)
        eval(fc[0])(*fc[1:])

def main():
    cur_lang, use_textarea, exec_as_function=sidebar()
    st.header("Augmentor Bar")
    if use_textarea:
        cmd = st.text_area("Command to execute", get_parse_skel(cur_lang))
    else:
        cmd=st.text_input("Command to execute", get_parse_skel(cur_lang))
    if cmd != '':
        # st.write(cmd)
        exec_func(cmd, exec_as_function)

if __name__ == '__main__':
    main()

