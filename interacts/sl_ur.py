import streamlit as st
import graphviz as graphviz
from interacts.viz_utils import traviz

lang='ur'
chunks=['''我们 学习 一门 语言 。
‫ہم ایک زبان سیکھ رہے ہیں-‬
hum aik zabaan seekh rahay hin-
''',
        '''这是 女老师 。
‫یہ استانی ہے-‬
yeh ustani hai -''',
        '''他们 学习 俄语 。
‫آپ روسی سیکھ رہے ہیں-‬
aap roosi seekh rahay hin-''',
        ]

# for chunk in chunks:
#     lines = chunk.split('\n')
#     prompt = f"{lines[2]} ({lines[0]})"
#     if st.checkbox(prompt):
#         g = traviz(chunk=chunk, lang=lang)
#         st.graphviz_chart(g)

# g = traviz(chunk=chunks[0], lang=lang)
# st.graphviz_chart(g)
# st.graphviz_chart(traviz(chunk=chunks[1], lang=lang))

for chunk in chunks:
    lines = chunk.split('\n')
    prompt = f"{lines[2]} ({lines[0]})"
    st.write(prompt)
    st.graphviz_chart(traviz(chunk=chunk, lang=lang))

