import streamlit as st
import altair as alt
from vega_datasets import data

# for the notebook only (not for JupyterLab) run this command once per session
alt.renderers.enable('notebook')

iris = data.iris()

st.write(alt.Chart(iris).mark_point().encode(
    x='petalLength',
    y='petalWidth',
    color='species'
))

