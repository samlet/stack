from functools import singledispatch
from decimal import Decimal
import streamlit as st

from augmentor.context import ctx

"""
add(1, 2)
add('Python', 'Programming')
add([1, 2, 3], [5, 6, 7])
add(1.23, 5.5)
add(Decimal(100.5), Decimal(10.789))
"""

@singledispatch
def add(a, b):
    raise NotImplementedError('Unsupported type')


@add.register(int)
def _(a, b):
    st.write("First argument is of type ", type(a))
    st.write(a + b)
    ctx['result_s'] = str(a + b)

@add.register(str)
def _(a, b):
    st.write("First argument is of type ", type(a))
    st.write(a + b)
    ctx['result_s']=str(a+b)

@add.register(list)
def _(a, b):
    st.write("First argument is of type ", type(a))
    st.write(a + b)
    ctx['result_s'] = str(a + b)

@add.register(float)
@add.register(Decimal)
def _(a, b):
    st.write("First argument is of type ", type(a))
    st.write(a + b)
    ctx['result_s'] = str(a + b)

exports={add}
