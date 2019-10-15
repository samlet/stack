import streamlit as st
import json

@st.cache
def get_states():
    # with urllib.request.urlopen(
    #         'https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_hash.json') as response:
    #     states = json.loads(response.read().decode())
    with open('/pi/ai/streamlit/states_hash.json') as f:
        states = json.loads(f.read())
    return states
