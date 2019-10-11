import streamlit as st
from sagas.nlu.uni_remote_viz import viz_sample
from sagas.conf.conf import cf

st.sidebar.title("Interactive services")
langs={"en":("English", "Mark Zuckerberg is the CEO of Facebook."),
       'zh':("Chinese", '最近的加油站在哪里 ?'),
       'fa':('Persian', '‫نزدیکترین ‫پمپ بنزین بعدی کجاست؟‬'),
       'it':('Italian', 'Anche questi sono sei mesi.'),
       'de':('German', 'Die Aufnahmen begannen im November.'),
       }

lang_labels=[v[0] for v in langs.values()]
cur_lang_name = st.sidebar.selectbox("Language", lang_labels)
cur_lang, default_text=[(k,v[1]) for k,v in langs.items() if v[0]==cur_lang_name][0]

text = st.text_area("Text to analyze", default_text)
st.write(f"Parse text as language {cur_lang}: {text}")
g=viz_sample(cur_lang, text, engine=cf.engine(cur_lang))
st.graphviz_chart(g)





