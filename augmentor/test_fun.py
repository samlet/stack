from functools import singledispatch
from decimal import Decimal
import streamlit as st

@singledispatch
def fun(arg, verbose=False):
    if verbose:
        st.write("Let me just say,", end=" ")
    st.write(arg)

@fun.register
def _(arg: int, verbose=False):
    if verbose:
        st.write("Strength in numbers, eh?", end=" ")
    st.write(arg)

@fun.register
def _(arg: list, verbose=False):
    if verbose:
        st.write("Enumerate this:")
    for i, elem in enumerate(arg):
        st.write(i, elem)

@fun.register(complex)
def _(arg, verbose=False):
    if verbose:
        st.write("Better than complicated.", end=" ")
    st.write(arg.real, arg.imag)

def nothing(arg, verbose=False):
    st.write("Nothing.")

fun.register(type(None), nothing)

@fun.register(float)
@fun.register(Decimal)
def fun_num(arg, verbose=False):
    if verbose:
        st.write("Half of your number:", end=" ")
    st.write(arg / 2)

exports={fun}
