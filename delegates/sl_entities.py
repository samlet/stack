import streamlit as st
from sagas.ofbiz.entities import OfEntity as e, \
    create_data_frame, create_relation_data_frame, \
    entity, record_list_df, finder

DEFAULT_ENT = "Shipment"

def entity_meta(ent_name):
    # meta_df=e('meta').Shipment
    meta_df=create_data_frame(ent_name)
    return meta_df

st.sidebar.title("Interactive entities")
offset, limit = st.sidebar.slider("Entity list data?", 0, 100, [0, 20])

ent_name = st.text_input("Entity model to analyze", DEFAULT_ENT)
meta_df=entity_meta(ent_name)
st.dataframe(meta_df)
if st.button("Show relations"):
    st.dataframe(create_relation_data_frame(ent_name))

if st.button("Show data"):
    result = finder.find_list(ent_name, limit, offset)
    result = record_list_df(ent_name, result)
    st.dataframe(result)

