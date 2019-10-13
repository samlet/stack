import streamlit as st

import io_utils
import sagas
from interacts.tracker_streamlit import enable_streamlit_tracker
from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.uni_remote_viz import viz_sample
from sagas.conf.conf import cf
import glob
from interacts.sl_utils import all_labels

enable_streamlit_tracker()

st.write("<style>red{color:red} orange{color:orange} "
         "yellow{color:yellow} green{color:green} "
         "blue{color:blue} purple{color:purple} "
         "cyan{color:blue} magenta{color:magenta} "
         "</style>", unsafe_allow_html=True)

language = st.sidebar.selectbox(
    'Which language do you choose?',
     list(all_labels.keys()))

cur_lang=all_labels[language]
corpus=[f for f in glob.glob(f'*_{cur_lang}_*.txt')]
df=sagas.to_df(corpus, ['file'])

cur_file = st.sidebar.selectbox(
    'Which corpus do you choose?',
     df['file'])
st.sidebar.text(f"Current: {cur_lang}, {cur_file}")

tools=NluTools()
# tools.clip_parse('fi', 'Tuolla ylhäällä asuu vanha nainen.')

lang=cur_lang
# text='Tuolla ylhäällä asuu vanha nainen.'

def show_file(file):
    text_raw=io_utils.read_file(file).split('►')

    rows=[]
    for t in text_raw:
        # st.write(t)
        rows.append([l for l in t.split('\n') if l.strip() != '' and not l.startswith('#') and not l.startswith('⊕') ])

    if st.checkbox('Sentences list'):
        if len(rows[0])==2:
            st.write(sagas.to_df(rows, ['translate', 'raw']))
        else:
            st.write(sagas.to_df(rows, ['translate', 'raw', 'translit']))
    return rows

# rows=show_file('en_fi_Adjectives.txt')
rows=show_file(cur_file)
for row in rows:
    text=row[1]
    if st.button(f"{text} ✁ {row[0]}"):
        engine = cf.engine(lang)
        g = viz_sample(lang, text, engine='corenlp', enable_contrast=True)
        st.graphviz_chart(g)
        tools.contrast(text, lang)
