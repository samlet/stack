import io_utils

normal_cnt="""import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

def main():
    sidebar()
    st.subheader("Application")

if __name__ == '__main__':
    main()

"""

class StreamlitCreator(object):
    def normal(self, file):
        """
        $ python -m sagas.tool.creators normal ./out/xxx.xx
        :param file:
        :return:
        """
        if not io_utils.exists(file):
            io_utils.write_to_file(file, normal_cnt)
            print(f"file {file} doesn't exists, create it")

if __name__ == '__main__':
    import fire
    fire.Fire(StreamlitCreator)

