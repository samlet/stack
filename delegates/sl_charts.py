import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

import pandas as pd
import numpy as np

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

# https://streamlit.io/docs/api.html#display-charts

def line_charts():
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

def bar_charts():
    chart_data = pd.DataFrame(
        [[20, 30, 50]],
        columns=['a', 'b', 'c'])

    st.bar_chart(chart_data)

def main():
    sidebar()
    st.subheader("Charts")

    line_charts()
    bar_charts()

if __name__ == '__main__':
    main()

