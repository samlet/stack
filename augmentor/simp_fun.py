from functools import singledispatch
import streamlit as st

@singledispatch
def simp(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

@simp.register(str)
def _(arg, verbose=False):
    st.write(".. argument is of type ", type(arg))

exports={simp}

