from functools import singledispatch
import streamlit as st
import pandas as pd
import numpy as np

def demo_map():
    df = pd.DataFrame(
        # np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],  # san francisco
        # np.random.randn(1000, 2) / [50, 50] + [39.90, -116.40],
        np.random.randn(1000, 2) / [50, 50] + [40.70, -74.00],  # new york
        columns=['lat', 'lon'])

    st.map(df)

@singledispatch
def maps(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

@maps.register(str)
def _(arg, verbose=False):
    """demo map"""
    st.write(".. argument is of type ", type(arg))
    demo_map()

exports={maps}

