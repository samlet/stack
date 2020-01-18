import streamlit as st
import io_utils
import sagas
import glob
from interacts.sl_utils import all_labels

# corpus=[('zh_fa_006.txt'),
#         ('en_fa_006.txt'),
#         ('zh_fa_041.txt'),
#         ]

st.sidebar.title("Interactive visualizer")

default_labels = ["Dutch", "Persian", "Afrikaans"]
langs = st.sidebar.multiselect(
    "Available langs", list(all_labels.keys()), default_labels
)
sel_langs={all_labels[l] for l in langs}

def is_sel(f):
    for l in sel_langs:
        if f"_{l}_" in f:
            return True
    return False

corpus=[f for f in glob.glob('*.txt') if is_sel(f)]
df=sagas.to_df(corpus, ['file'])

option = st.sidebar.selectbox(
    'Which corpus do you choose?',
     df['file'])

cur_lang=option[3:5]
'Current corpus:', option, f", language code: {cur_lang}", f", available lang: {langs}"

# text_raw=''''''.split('►')
text_raw=io_utils.read_file(option).split('►')

rows=[]
for t in text_raw:
    # st.write(t)
    rows.append([l for l in t.split('\n') if l.strip() != '' and not l.startswith('#') and not l.startswith('⊕') ])

if len(rows[0])==2:
    st.write(sagas.to_df(rows, ['translate', 'raw']))
else:
    st.write(sagas.to_df(rows, ['translate', 'raw', 'translit']))

# print(len(text_raw))
# el=[l for l in text_raw[0].split('\n') if l.strip()!='']
# print(el[0], '..', el[2])
# print(el[1])

@st.cache
def dia(el):
    from sagas.nlu.corenlp_helper import LangDialect as dia
    exprs = []
    fn=lambda s: dia(cur_lang, local_translit=True, outf=lambda x: exprs.append(x)).ana(s)
    return fn(el[1]), exprs

for text in text_raw:
    el = [l for l in text.split('\n') if l.strip() != '']
    st.write(f"ʘ‿ʘ {el[1]}")
    prompt = f"{el[2]} ({el[0]})" if len(el)>=3 else f"ref: {el[0]}"
    st.write(prompt)

    gra, exprs=dia(el)
    for e in exprs:
        st.write(e)
    st.graphviz_chart(gra)

