import streamlit as st

from interacts.sl_utils import all_labels
from sagas.nlu.nlu_cli import get_chains, get_word_sets


def display_chains(word, lang='en', pos='*'):
    resp = get_word_sets(word, lang, pos)
    word_descs={}
    if resp['result'] == 'success':
        sets = resp['data']
        for s in sets:
            # for exa in s['examples']:
            #     print('\t', exa)
            word_descs[s['name']] ={'def':s['definition'], 'examples':s['examples']}

        resp = get_chains(word, lang, pos)
        if len(resp) > 0:
            for chain in resp:
                syn_name=chain['name']
                st.markdown("`%s` **%s**" % (chain['offset'],syn_name))
                syns=chain['chain']
                desc=word_descs[syn_name]['def']
                opts = st.multiselect(
                    desc, list(syns), [syns[0]]
                )
                st.write(opts)
        else:
            st.write('none.')

def display_lang_selector():
    language = st.sidebar.selectbox(
        'Which language do you choose?',
         list(all_labels.keys()))

    cur_lang=all_labels[language]
    return cur_lang

def main():
    st.subheader("Word Mappings")
    text = st.text_input("Word to analyze", 'ship')
    cur_lang=display_lang_selector()
    display_chains(text, cur_lang)

if __name__ == "__main__":
    main()

