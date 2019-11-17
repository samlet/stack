from functools import singledispatch
import streamlit as st

from sagas.conf.conf import cf

cf.enable_opt('print_not_matched')

"""
rule patterns:
    rule('Shenzhen ist das Silicon Valley für Hardware-Firmen', 'de')
        entire(intentof('tech', 0.6, True))
    rule('They read these newspapers.', 'en')
        verb(nsubj=agency, obj=kindof('print_media/artifact', 'n'))
"""

def dynamic_rule(data, rule_str):
    from sagas.nlu.inspectors import InspectorFixture
    from sagas.nlu.inspectors import NegativeWordInspector as negative
    from sagas.nlu.inspectors import DateInspector as dateins
    from sagas.nlu.inspectors import EntityInspector as entins
    from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
    from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
    from sagas.nlu.inspector_rasa import RasaInspector as intentof

    from sagas.nlu.patterns import Patterns, print_result

    ft=InspectorFixture()
    domains, meta=ft.request_domains(data)
    agency = ['c_pron', 'c_noun']
    rs=eval(f"[Patterns(domains, meta, 5).{rule_str}]")
    print_result(rs)

@singledispatch
def rule(text, lang, verbose=False):
    raise NotImplementedError('Unsupported type')

@rule.register(str)
def _(text, lang, verbose=False):
    from augmentor.viz_fun import parse_deps
    # st.write(".. argument is of type ", type(arg))
    # st.write({'a':'b'})
    if st.checkbox('Display parse result'):
        parse_deps(text, lang, translit=None)

    data = {'lang': lang, "sents": text}
    # rule_str like: "entire(intentof('tech', 0.6, True))"
    rule_str=st.text_input("Input rule", '')
    if rule_str!='':
        dynamic_rule(data, rule_str)
        # st.text('✁', '-' * 30)

exports={rule}

