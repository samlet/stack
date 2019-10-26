from functools import singledispatch
import streamlit as st
import pandas as pd

# corpus('Around the house', 'ar')
# corpus_audio('Around the house', 'ja')
# corpus_audio('', 'ja')

@singledispatch
def corpus(arg, lang, verbose=False):
    raise NotImplementedError('Unsupported type')

def list_chapters(lang, chapters):
    dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
    del dfjson['audio']
    for name, group in dfjson.groupby('chapter'):
        if name in chapters:
            st.markdown(f"`{name}`")
            del group['chapter']
            st.table(group)

def list_audio_urls(lang, chapters):
    dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
    for name, group in dfjson.groupby('chapter'):
        if name in chapters:
            # st.markdown(f"`{name}`")
            st.subheader(name)
            # st.table(group)
            for index, row in group.iterrows():
                st.markdown(f"`{row['text']}`")
                st.markdown(f"**{row['translit']}** {row['translate']}")
                st.audio(row['audio'])

@corpus.register(str)
def _(arg, lang, verbose=False):
    st.write(".. argument is of type ", type(arg))
    list_chapters(lang, [arg])

@singledispatch
def corpus_audio(arg, lang, verbose=False):
    raise NotImplementedError('Unsupported type')


def list_chapter_titles(lang):
    dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
    return [name for name, group in dfjson.groupby('chapter')]

@corpus_audio.register(str)
def _(arg, lang, verbose=False):
    st.write(".. argument is of type ", type(arg))
    chapters=[arg]
    if arg=='':
        chapters=list_chapter_titles(lang)
        chapter=st.selectbox('Chapters', chapters)
        chapters=[chapter]
    list_audio_urls(lang, chapters)

exports={corpus, corpus_audio}

