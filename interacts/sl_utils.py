import re
import streamlit as st

all_labels = {"Dutch":'nl', "Persian":'fa', "Japanese":'ja',
              "Korea":'ko', "Afrikaans":'af', "Russian":'ru',
              "Italian":'it', "Turkish":'tr', 'Finnish':'fi',
              'Estonian':'et',
              "Arabic":'ar'}

def fix_sents(text, lang):
    text = re.sub(r" ?\([^)]+\)", "", text)
    if lang in ('ja', 'zh'):
        text = text.replace(' ', '')
    return text

def write_styles():
    st.write("<style>red{color:red} orange{color:orange} "
             "yellow{color:yellow} green{color:green} "
             "blue{color:blue} purple{color:purple} "
             "cyan{color:blue} magenta{color:magenta} "
             "</style>", unsafe_allow_html=True)
