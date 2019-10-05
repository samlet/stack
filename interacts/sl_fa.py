import streamlit as st
import graphviz as graphviz
from interacts.viz_utils import traviz

lang='fa'
chunks=['''最近的 邮局 在哪？
‫نزدیکترین ‫پستخانه کجاست؟‬
postkhâne-ye ba-adi kojâst?''',
        '''我 有 一个 草莓 。
‫من یک توت فرنگی دارم.‬
man yek toot farangi dâram.
''',
        '''我 有 一个 猕猴桃 和 一个 甜瓜 。
‫من یک کیوی و یک خربزه دارم.‬
man yek kivi va yek khar-boze dâram.''',
        '''我 吃 一个 加 植物黄油 和 西红柿的 三明治 。
‫من ساندویچ با مارگارین و گوجه فرنگی می‌خورم.‬
man sândewich bâ mârgârin va goje farangi mikhoram.''',
        ]

for chunk in chunks:
    lines = chunk.split('\n')
    prompt = f"{lines[2]} ({lines[0]})"
    st.write(prompt)
    st.graphviz_chart(traviz(chunk=chunk, lang=lang))

