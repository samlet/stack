from functools import singledispatch
import streamlit as st

from augmentor.context import ctx


@singledispatch
def disp(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

@disp.register(str)
def _(arg, verbose=False):
    st.write(arg, ctx)

exports={disp}


