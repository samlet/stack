import streamlit as st
import graphviz as graphviz
from interacts.viz_utils import traviz

lang='hi'
chunks=['''学习 语言 是 很 有趣的 。
भाषाएँ सीखना दिलचस्प होता है
bhaashaen seekhana dilachasp hota hai''',
        '''我们 学习 一门 语言 。
हम एक भाषा सीख रहे हैं
ham ek bhaasha seekh rahe hain''',
        ]

for chunk in chunks:
    lines = chunk.split('\n')
    prompt = f"{lines[2]} ({lines[0]})"
    st.write(prompt)
    st.graphviz_chart(traviz(chunk=chunk, lang=lang))


