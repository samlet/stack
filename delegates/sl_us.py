import streamlit as st
from delegates.geo_helper import get_states
import html

states = get_states()

state = st.selectbox("State", options=list(states.keys()), format_func=lambda k: states.get(k), )

for k,v in states.items():
    vt=html.escape(f"https://arcos-api.ext.nile.works/v1/total_pharmacies_state?state={k}&key=WaPo")
    # st.markdown(f"- [{v}]({vt})")
    st.write(f'''<li><a href="{vt}" target="_blank" download="total_pharmacies_state_{k}">{v}</a>''', unsafe_allow_html=True)

