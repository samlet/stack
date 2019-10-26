import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

def shorten_audio_option(opt):
    return opt.split("/")[-1]

def play_mp3():
    src = "https://www.book2.nl/book2/RO/SOUND/0743.mp3"
    st.audio(src)

    # song = st.selectbox(
    #     "Pick an MP3 to play",
    #     (
    #         "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    #         "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    #         "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    #     ),
    #     0,
    #     shorten_audio_option,
    # )
    #
    # st.audio(song)

def main():
    sidebar()
    st.subheader("Application")

    play_mp3()

if __name__ == '__main__':
    main()

