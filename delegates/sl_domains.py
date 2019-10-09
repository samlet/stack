import streamlit as st

st.sidebar.title("Interactive domains")

all_labels = {"Party":'', "Order":''}
default_labels = ["Party", "Order"]
modules = st.sidebar.multiselect(
    "Available modules", list(all_labels.keys()), default_labels
)
sel_mods={all_labels[l] for l in modules}


