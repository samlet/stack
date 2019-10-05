import streamlit as st

# text_raw=''''''.split('►')
text_raw='''我们 在 哪里 ?
‫ما کجا هستیم؟‬
mâ kojâ hastim?
►
我们 在 学校 里 。
‫ما در مدرسه هستیم.‬
mâ dar madrese hastim.
►
我们 在 上课 。
‫ما کلاس داریم.‬
mâ kelâse dars dârim
►
 
 
 
 
这些 是 学生 。
‫اینها دانش آموزان کلاس هستند.‬
ânhâ dânesh-âmoozân hastand.
►
这是 女老师 。
‫این خانم معلم است.‬
in khânom-e moalem ast.
►
这是 班级/教室 。
‫این کلاس است.‬
in kelâse dars ast.
►
 
 
 
 
我们 做 什么 ?
‫چکار کنیم؟‬
mâ chekâr mikonim?
►
我们 学习 。
‫ما درس می‌خوانیم.‬
mâ dars mikhânim.
►
我们 学习 一门 语言 。
‫ما زبان یاد می‌گیریم.‬
mâ yek zabân yâd migirim.
►
 
 
 
 
我 学习 英语 。
‫من انگلیسی یاد می‌گیرم.‬
man engelisi yâd migiram.
►
你 学习 西班牙语 。
‫تو اسپانیایی یاد می‌گیری.‬
to espâni-â-i yâd migiri.
►
他 学习 德语 。
‫او (مرد) آلمانی یاد می‌گیرد.‬
oo âlmâni yâd migirad.
►
 
 
 
 
我们 学习 法语 。
‫ما فرانسوی یاد می‌گیریم.‬
mâ farânsavi yâd migirim.
►
你们 学习 意大利语 。
‫شما ایتالیایی یاد می‌گیرید.‬
shomâ itâli-â-i yâd migirid.
►
他们 学习 俄语 。
‫آنها روسی یاد می‌گیرند.‬
ânhâ rusi yâd migirand.
►
 
 
 
 
学习 语言 是 很 有趣的 。
‫یادگیری زبان، کار جالبی است.‬
yâd-giri-ye zabân jâleb ast.
►
我们 要 理解/听懂 人们 (讲话) 。
‫ما می‌خواهیم حرفهای مردم را بفهمیم.‬
mâ mikhâ-him ensânhâ râ befahmim.
►
我们 想 和 人们 说话/交谈 。
‫ما می‌خواهیم با مردم صحبت کنیم.‬
mâ mikhâ-him bâ ensânhâ sohbat konim.
'''.split('►')

# print(len(text_raw))
# el=[l for l in text_raw[0].split('\n') if l.strip()!='']
# print(el[0], '..', el[2])
# print(el[1])

@st.cache
def dia(el):
    import sagas
    fn=lambda s: sagas.dia('fa', local_translit=True).ana(s)
    return fn(el[1])

for text in text_raw:
    el = [l for l in text.split('\n') if l.strip() != '']
    prompt = f"{el[2]} ({el[0]})"
    st.write(prompt)
    st.graphviz_chart(dia(el))

