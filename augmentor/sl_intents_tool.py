import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
from sagas.nlu.utils import fix_sents

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()
    return cur_lang

def get_all_intents():
    from sagas.tool.intents_tool import intents_tool
    rs = intents_tool.db.corpus.find({'$and': [
        {"intent": {'$not': {'$size': 0}}},
        {"intent": {'$exists': True}}
    ]})
    rm = {r['text']: r['intent'] for r in rs}
    return {r for r in rm.values()}

def get_records(lang, chapter, field, fix=False):
    from sagas.tool.intents_tool import intents_tool
    text_list = [(doc[field] if not fix else fix_sents(doc[field], lang),
                  doc['text'] if lang != 'en' else f"{doc['chapter'].lower()[:10]}_{doc['index']}",
                  doc['intent'] if 'intent' in doc else '',
                  )
                 for doc in intents_tool.db.corpus.find({'chapter': chapter})]
    return text_list

def intents_tool_panel(lang):
    from sagas.tool.intents_tool import intents_tool
    import sagas

    item=intents_tool.get_chapters()
    chapter=st.selectbox('which chapter to modify', item['chapters'])
    field = f'lang_{lang}' if lang != 'en' else 'text'
    text_list=get_records(lang, chapter, field)
    opts = [t[0] for t in text_list if t[2] == '']

    # intent modify function only available when the lang==en
    if lang=='en' and len(opts)>0:
        sents=st.selectbox('which sentence to modify', opts )
        entry=next(t for t in text_list if t[0]==sents)
        st.markdown(f"{entry[0]} `{entry[2]}`")

        sel_intents=st.multiselect('choose or input a intent', list(get_all_intents()))
        st.write(sel_intents)
        text_intent=st.text_input("intent", sel_intents[0] if len(sel_intents)>0 else '')
        if text_intent.strip()!='':
            # sel_intents.append(text_intent)
            target_intent=text_intent.strip()
        elif len(sel_intents)>0:
            target_intent=sel_intents[0]
        else:
            target_intent=None

        if target_intent is not None:
            if st.button("store"):
                st.write(f'.. store {target_intent}')
                intents_tool.set_intent_by_text(sents, target_intent)

                # refresh list
                text_list = get_records(lang, chapter, field)

    # for entry in text_list:
    #     st.markdown(f"{entry[0]} `{entry[1]}`")
    st.table(sagas.to_df(text_list,
                         columns=[f'text_{lang}', 'text_en' if lang!='en' else 'location', 'intent']))

def main():
    lang=sidebar()
    st.subheader("intents tool")
    intents_tool_panel(lang)

if __name__ == '__main__':
    main()

