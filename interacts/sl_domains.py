import streamlit as st
import re
import io_utils
import sagas
from interacts.tracker_streamlit import enable_streamlit_tracker
from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.uni_remote_viz import list_chunks, display_doc_deps
from sagas.nlu.uni_remote import dep_parse
from sagas.conf.conf import cf
import glob
from interacts.sl_utils import all_labels, fix_sents, write_styles

enable_streamlit_tracker()
write_styles()

corpus_prefix='/pi/stack/interacts'

def choose_lang_and_corpus():

    language = st.sidebar.selectbox(
        'Which language do you choose?',
         list(all_labels.keys()))

    cur_lang=all_labels[language]
    corpus=[f for f in glob.glob(f'{corpus_prefix}/*_{cur_lang}_*.txt')]
    df=sagas.to_df(corpus, ['file'])

    cur_file = st.sidebar.selectbox(
        'Which corpus do you choose?',
         df['file'],
        format_func=lambda k: k.replace(corpus_prefix+'/', '').replace('.txt', '') ,
    )
    st.sidebar.text(f"Current: {cur_lang}, {cur_file}")
    return cur_lang, cur_file

cur_lang, cur_file= choose_lang_and_corpus()

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

display_translit=st.sidebar.checkbox('Display translit')

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

def row_view(row):
    text = row[1]
    if display_translit and len(row) > 2:
        label = row[2]
    else:
        label = text
    if st.button(f"{label} ✁ {row[0]}"):
        text = fix_sents(text, lang)
        engine = get_engine(lang)
        # g = sentence_view(lang, text, engine=engine, translit_lang=lang, enable_contrast=True)
        doc_jsonify, resp = dep_parse(text, lang, engine, ['predicts'])
        if doc_jsonify is not None:
            list_chunks(doc_jsonify, resp, lang, enable_contrast=True)
            g=display_doc_deps(doc_jsonify, resp, translit_lang=lang)

            st.graphviz_chart(g)
            if len(row) > 2:
                st.text(f"♤ {row[2]}")

            words = [word.text for word in doc_jsonify.words]
            tools.contrast(text, lang, word_map=words)

# rows=show_file('en_fi_Adjectives.txt')
rows=show_file(cur_file)
for row in rows:
    # text=re.sub(r" ?\([^)]+\)", "", row[1])
    row_view(row)



