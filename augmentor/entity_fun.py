from functools import singledispatch
from decimal import Decimal
import streamlit as st

from sagas.ofbiz.entities import OfEntity as e, \
    create_data_frame, create_relation_data_frame, \
    entity, record_list_df, finder

@singledispatch
def ent(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

def entity_meta(ent_name):
    # meta_df=e('meta').Shipment
    meta_df=create_data_frame(ent_name)
    return meta_df

@ent.register(str)
def _(arg, verbose=False):
    # st.write(arg)
    ent_name=arg
    offset, limit = st.sidebar.slider("Entity list data?", 0, 100, [0, 20])
    meta_df = entity_meta(ent_name)
    st.dataframe(meta_df)
    if st.button("Show relations"):
        st.dataframe(create_relation_data_frame(ent_name))

    if st.button("Show data"):
        result = finder.find_list(ent_name, limit, offset)
        result = record_list_df(ent_name, result)
        st.dataframe(result)


@singledispatch
def browse(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

@browse.register(str)
def _(arg, verbose=False):
    ent_name = arg
    offset, limit = st.sidebar.slider("Entity list data?", 0, 100, [0, 20])
    result = finder.find_list(ent_name, limit, offset)
    result = record_list_df(ent_name, result)
    st.dataframe(result)

exports={ent, browse}
