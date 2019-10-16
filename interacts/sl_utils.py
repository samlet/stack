import re
import streamlit as st
from sagas.conf.conf import cf

# all_labels = {"Dutch":'nl', "Persian":'fa', "Japanese":'ja',
#               "Korea":'ko', "Afrikaans":'af', "Russian":'ru',
#               "Italian":'it', "Turkish":'tr', 'Finnish':'fi',
#               'Estonian':'et',
#               "Arabic":'ar'}
# def all_labels():
from sagas.nlu.treebanks import treebanks
from sagas.nlu.utils import fix_sents

all_labels=treebanks.lang_map()

def write_styles():
    st.write("<style>red{color:red} orange{color:orange} "
             "yellow{color:yellow} green{color:green} "
             "blue{color:blue} purple{color:purple} "
             "cyan{color:blue} magenta{color:magenta} "
             "</style>", unsafe_allow_html=True)

def fix_data(data):
    if 'engine' not in data:
        data['engine'] = cf.engine(data['lang'])
    data['sents']=fix_sents(data['sents'], data['lang'])
    return data
