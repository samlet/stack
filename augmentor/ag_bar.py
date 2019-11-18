import streamlit as st

from augmentor.context import ctx
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
from augmentor.display_fun import disp
from augmentor.parse_fun import parse, domains
from augmentor.entity_fun import ent, browse
from augmentor.chart_fun import chart
from augmentor.maps_fun import maps
from augmentor.viz_fun import viz
from augmentor.corpus_fun import corpus, corpus_audio
from augmentor.product_fun import product
from augmentor.rules_fun import rule
from augmentor.odoo_fun import odoo_list
# -----------

enable_streamlit_tracker()
write_styles()

def flows():
    st.sidebar.header("Flows")
    fns=['add(5,5)', 'fun(5)', "disp('result:')",
         "maps('new york')",
         "browse('Person')",
         "viz('我要确认我预定的航班 。', 'zh')",
         "corpus_audio('', 'ja')",
         "parse('저는 양파를 안 좋아해요.', 'ko')",
         "domains('')",
         "domains('Die Aufnahmen begannen im November.', 'de')",
         """product("GZ-2002", 'price')""",
         '''product(dt('2013-07-04 00:00:00'), "Test_product_A")''',
         "odoo_list('products')",
         "odoo_list('stock_picking')",
         ]
    default_labels = ['add(5,5)', "disp('result:')"]
    labels = st.sidebar.multiselect(
        "Shortcuts", fns, default_labels
    )
    return labels

def sidebar():
    cur_lang=display_lang_selector()
    use_textarea=st.sidebar.checkbox('Use textarea', value=True)
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
        # exec(cmd, globals(),locals())
        exec(cmd)
        st.markdown(f"**➴ result** `{ctx['result_s']}`")
    else:
        fc = shlex.split(cmd)
        eval(fc[0])(*fc[1:])

def main():
    st.header("Augmentor Bar")

    cur_lang, use_textarea, exec_as_function=sidebar()
    labels=flows()
    if st.sidebar.button('Execute flows'):
        st.sidebar.text(labels)
        exec_func('\n'.join(labels), exec_as_function=True)
    else:
        if use_textarea:
            cmd = st.text_area("Command to execute", get_parse_skel(cur_lang))
        else:
            cmd=st.text_input("Command to execute", get_parse_skel(cur_lang))
        if cmd != '':
            # st.write(cmd)
            exec_func(cmd, exec_as_function)

if __name__ == '__main__':
    main()

