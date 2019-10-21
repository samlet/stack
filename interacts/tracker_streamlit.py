from sagas.runtime import runtime
from sagas.tracker_intf import TrackerIntf
import streamlit as st
from sagas.nlu.env import sa_env
import html

def flat_args(args):
    return [str(arg) for arg in args]

class StreamlitImpl(TrackerIntf):
    def info(self, *args, sep=' ', end='\n', file=None):
        st.text(sep.join(flat_args(args)))

    def important(self, *args):
        st.markdown(f"**{' '.join(flat_args(args))}**")

    def emphasis(self, color, *args):
        # print(colored(' '.join(args), color))
        # st.markdown(f"**{' '.join(args)}**")
        text=' '.join(flat_args(args))
        if text.startswith('\t'):
            indent='<li>'
        else:
            indent=''
        text=html.escape(text).replace('[', '「').replace(']', '」')
        st.write(f"{indent}<small><{color}>{text}</{color}></small>", unsafe_allow_html=True)

    def dfs(self, *args):
        for arg in args:
            st.dataframe(arg)

    def gv(self, dot):
        st.graphviz_chart(dot)

    def label_text(self, k, *args):
        color='green'
        st.write(f"<{color}>{k}:</{color}> {' '.join(args)}", unsafe_allow_html=True)

    def write(self, *args):
        st.write(*args)

streamlit_inst=StreamlitImpl()
def enable_streamlit_tracker():
    """
    >>> from interacts.tracker_streamlit import enable_streamlit_tracker
    >>> enable_streamlit_tracker()
    :return:
    """
    sa_env.runtime='streamlit'
    runtime.tracker=streamlit_inst



