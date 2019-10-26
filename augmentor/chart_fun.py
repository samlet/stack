from functools import singledispatch
import streamlit as st
import pandas as pd

@singledispatch
def chart(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

@chart.register(str)
def _(arg, verbose=False):
    st.write(".. argument is of type ", type(arg))

    chart_data = pd.DataFrame(
        [[20, 30, 50]],
        columns=['a', 'b', 'c'])
    st.bar_chart(chart_data)

@chart.register(dict)
def _(arg, verbose=False):
    cols=[]
    vals=[]
    for k,v in arg.items():
        cols.append(k)
        vals.append(v)
    chart_data = pd.DataFrame([vals], columns=cols)
    st.bar_chart(chart_data)

exports={chart}

