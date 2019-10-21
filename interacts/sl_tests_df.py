import streamlit as st
import pandas as pd
import numpy as np

from interacts.common import display_lang_selector
# from interacts.map_store import map_store
from interacts.json_store import json_store
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

def df_tests():
    df1 = pd.DataFrame(
        np.random.randn(3, 20),
        columns=('col %d' % i for i in range(20)))

    my_table = st.table(df1)

    if st.button('Add rows'):
        df2 = pd.DataFrame(
            np.random.randn(3, 20),
            columns=('col %d' % i for i in range(20)))

        my_table.add_rows(df2)

def df_tests_2():
    # Create a table to be styled in various ways
    np.random.seed(24)
    df = pd.DataFrame({"A": np.linspace(1, 5, 5)})
    df = pd.concat([df, pd.DataFrame(np.random.randn(5, 4), columns=list("BCDE"))], axis=1)
    df.iloc[0, 2] = np.nan

    st.subheader("Unstyled")
    st.table(df)
    #
    st.subheader("Add rows")
    x = st.table(
        df.style.set_properties(**{"background-color": "black", "color": "lawngreen"})
    )
    if st.button('Add a row 1'):
        x.add_rows(
            pd.DataFrame(np.random.randn(3, 5)).style.set_properties(
                **{"background-color": "lawngreen", "color": "black"}
            )
        )
    if st.button('Add a row 2'):
        x.add_rows(
            pd.DataFrame(np.random.randn(2, 5)).style.format(
                lambda value: "" if value > 0 else "*"
            )
        )

    w2 = st.slider("rows", 0, 10, 1)
    st.write(w2)
    if st.button('Change'):
        # 每次增加时, 实际上需要生成一个df, 这个新df将包含每一次增加的元素, 相当于是一个place-holder.
        x.add_rows(
            pd.DataFrame(np.random.randn(w2, 5)).style.format(
                lambda value: "" if value > 0 else "*"
            )
        )

def df_placeholder():
    my_placeholder = st.empty()
    # df1=json_store.get_df()
    # df1 = pd.DataFrame(
    #     np.random.randn(3, 20),
    #     columns=('col %d' % i for i in range(20)))

    my_placeholder.table(json_store.get_df())

    # 当slider值变动时, df就会重新载入; 所以df的初始值可以从其它地方载入, 比如redis, 而每一次更新,
    # 也是要更新redis的.
    # w2 = st.slider("rows", 0, 10, 1)
    # st.write(w2)

    # st.subheader("Radio")
    # options = ("female", "male")
    # w5 = st.radio("Gender", options, 1)
    # st.write(w5)

    st.subheader("Field mappings")
    fields=['nsubj', 'obl', 'obj']
    opts = st.multiselect(
        'Selected fields', fields, [fields[0]]
    )
    opt_vals={}
    for field in opts:
        options = ("date time", "entity", "intent")
        type = st.selectbox(f"Map field {field} as", options, 0)

        if type=='intent':
            extract=st.text_input('Extract intent', 'default')
        elif type=='entity':
            extract=st.text_area('Extract entities (one entity per line)', 'default')
        else:
            extract=''
        opt_vals[field] = {'type':type, 'value':extract.replace('\n', ',')}

    if st.button('Change'):
        # my_placeholder.table(pd.DataFrame(np.random.randn(w2, 5)).style.format(
        #         lambda value: "" if value > 0 else "*"
        #     ))
        json_store.modify()
        my_placeholder.table(json_store.get_df())

    st.write(opt_vals)
    if st.button('Add a record'):
        json_store.add()
        my_placeholder.table(json_store.get_df())

    if st.button('Clear'):
        json_store.clear()
        my_placeholder.table(json_store.get_df())


def main():
    sidebar()
    st.subheader("Data frame Application")
    # df_tests()
    # df_tests_2()
    df_placeholder()

if __name__ == '__main__':
    main()

