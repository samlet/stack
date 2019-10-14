import streamlit as st
import re
import io_utils
import sagas
from interacts.tracker_streamlit import enable_streamlit_tracker
from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.uni_remote_viz import viz_sample
from sagas.conf.conf import cf
import glob
from interacts.sl_utils import all_labels, fix_sents

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

# options
engine_specs={}
def set_engine(l,e):
    engine_specs[l]=e
    return True

operators={'corenlp(ja)': lambda: set_engine('ja', 'corenlp'),
           'corenlp(ar)': lambda: set_engine('ar', 'corenlp'),
           'spacy(en)': lambda: set_engine('en', 'spacy'),
           }
default_opts={'corenlp(ar)'}
opts = st.sidebar.multiselect(
    "Available options", list(operators.keys()), default_opts
)
for opt in opts:
    operators[opt]()

# process
tools=NluTools()
# tools.clip_parse('fi', 'Tuolla ylhäällä asuu vanha nainen.')

lang=cur_lang
# text='Tuolla ylhäällä asuu vanha nainen.'

def show_file(file):
    text_raw=io_utils.read_file(file).split('►')
    if st.checkbox('References'):
        links=[l.strip().split('\n')[0] for l in text_raw if l.strip().startswith('⊕')]
        # st.text(f"{len(links)}")
        for link in links:
            print(link)
            st.markdown(link)
            # st.text(link)

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

def get_engine(lang):
    if lang in engine_specs:
        return engine_specs[lang]
    return cf.engine(lang)

# rows=show_file('en_fi_Adjectives.txt')
rows=show_file(cur_file)
for row in rows:
    # text=re.sub(r" ?\([^)]+\)", "", row[1])
    text=row[1]
    if st.button(f"{text} ✁ {row[0]}"):
        text = fix_sents(text, lang)
        engine = get_engine(lang)
        g = viz_sample(lang, text, engine=engine, translit_lang=lang, enable_contrast=True)
        st.graphviz_chart(g)
        if len(row)>2:
            st.text(f"♤ {row[2]}")
        tools.contrast(text, lang)

