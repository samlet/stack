import streamlit as st
import json
from sagas.conf.conf import cf

@st.cache
def get_states():
    # with urllib.request.urlopen(
    #         'https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_hash.json') as response:
    #     states = json.loads(response.read().decode())
    with open(f'{cf.conf_dir}/ai/streamlit/states_hash.json') as f:
        states = json.loads(f.read())
    return states
