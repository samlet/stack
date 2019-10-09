import streamlit as st
from sagas.nlu.uni_remote_viz import viz_sample
rg=viz_sample('zh', '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制。', 'ltp')
st.write(rg)
