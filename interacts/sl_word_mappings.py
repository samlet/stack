import streamlit as st

from interacts.common import display_lang_selector
from interacts.nlu_parsers import procs_sents
from interacts.sl_utils import all_labels
from sagas.nlu.nlu_cli import get_chains, get_word_sets


def display_chains(word, lang='en', pos='*'):
    resp = get_word_sets(word, lang, pos)
    word_descs={}
    opts=[]
    if resp['result'] == 'success':
        sets = resp['data']
        for s in sets:
            # for exa in s['examples']:
            #     print('\t', exa)
            word_descs[s['name']] ={'def':s['definition'], 'examples':s['examples']}

        resp = get_chains(word, lang, pos)
        if len(resp) > 0:
            states={c['name']:f"{c['name']} - {word_descs[c['name']]['def']}" for c in resp}
            state = st.selectbox("Chains", options=list(states.keys()),
                                 format_func=lambda k: states.get(k), )
            for chain in resp:
                syn_name=chain['name']
                if syn_name==state:
                    st.markdown("`%s` **%s**" % (chain['offset'],syn_name))
                    syns=chain['chain']
                    desc=word_descs[syn_name]['def']
                    opts = st.multiselect(
                        desc, list(syns), [syns[0]]
                    )
                    st.write(opts)
        else:
            st.write('none.')
    return opts


def sentence_part(cur_lang):
    # 彼女は 美人な だけでなく 、 頭も いい です 。
    text = st.text_area("Sentence to analyze", '')
    if text != '':
        json_r = procs_sents(text, cur_lang)
        syns = [s for c in json_r for s in c['synsets']]
        words = [(s['word'], s['indicator']) for s in syns]
        # st.write(words)
        sels={}
        for i, word in enumerate(words):
            st.subheader(f"{i} - {word[1]}: {word[0]}")
            opt_res=display_chains(word[0], cur_lang)
            sels[f"{i} - {word[1]}/{word[0]}"]=(word, opt_res)
        opts=st.multiselect('Available parts', list(sels.keys()), [])
        if st.checkbox("Show full response json .."):
            st.write(json_r)
        if st.button("Save to rule"):
            # st.write({sels[opt][0]:sels[opt][1] for opt in opts})
            st.write([(opt, '/'.join(sels[opt][1])) for opt in opts])

def main():
    header=st.header("Word Mappings")
    cur_lang=display_lang_selector()

    app_mode = st.sidebar.selectbox("Choose the app mode",
                                    ["Word mappings",
                                     "Sentence parser",
                                     ])
    header.header(app_mode)
    if app_mode == "Word mappings":
        # st.sidebar.success('To continue select "Run the app".')
        text = st.text_input("Word to analyze", 'ship')
        display_chains(text, cur_lang)
    elif app_mode == "Sentence parser":
        sentence_part(cur_lang)


if __name__ == "__main__":
    main()

