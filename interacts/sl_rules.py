import streamlit as st

from interacts.sl_utils import write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
from sagas.tool.misc import get_verb_domains
enable_streamlit_tracker()

write_styles()

dataset=[{'lang': 'de', "sents": 'Die Aufnahmen begannen im November.', 'engine':'corenlp'},
         {'lang': 'ko', "sents": '언어를 배우는 것은 흥미로워요.', 'engine':'corenlp'},
         ]
# data = {'lang': 'de', "sents": 'Die Aufnahmen begannen im November.', 'engine':'corenlp'}
for data in dataset:
    if st.button(data['sents']):
        _=get_verb_domains(data)

