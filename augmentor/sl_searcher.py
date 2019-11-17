import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
from interacts.sl_utils import all_labels
import sagas.tracker_fn as tc
import json

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

def select_langs():
    default_labels = ["Dutch", "Persian", "Afrikaans"]
    langs = st.sidebar.multiselect(
        "Available langs", list(all_labels.keys()), default_labels
    )
    sel_langs = {all_labels[l] for l in langs}
    return sel_langs

def parse_controls(results):
    rs=[]
    for lang,v in results.items():
        for sent in v:
            st.markdown(f"{sent['translate']} `{sent['translit']}`")
            rs.append((sent['translate'], lang, sent['translit']))
    return rs

def corpus_search_bar():
    from sagas.corpus.searcher import CorpusSearcher, search_in_list
    from augmentor.viz_fun import parse_deps

    text = st.text_input("Input a sentence", "I eat rice")
    langs=select_langs()
    top_result = st.number_input('Insert a number', value=5)

    searcher=CorpusSearcher(model_file='/pi/stack/spacy-2.2/data/embedded_corpus.pkl')
    relevant_quotes, relevant_chapters = searcher.search(text, ['text', 'chapter'], top_result)
    for q in range(top_result):
        # tc.emp('magenta', '>' + relevant_quotes[q])
        st.subheader('>' + relevant_quotes[q])
        tc.emp('green', relevant_chapters[q])

        if langs is not None:
            # search_in_list('I write a letter.', ['ja', 'fa', 'id'])
            results = search_in_list(relevant_quotes[q], langs)
            if st.checkbox(f"{q}. show result in lang {', '.join(langs)}"):
                st.write(results)
            sent_rs=parse_controls(results)
            if st.button(f"{q}. parse sents in lang {', '.join(langs)}"):
                for sent in sent_rs:
                    parse_deps(sent[0], sent[1], sent[2])

    searcher.end()

def main():
    sidebar()
    st.subheader("Corpus Searcher")
    corpus_search_bar()

if __name__ == '__main__':
    main()

