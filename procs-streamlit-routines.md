# procs-streamlit-routines.md
⊕ [API reference — Streamlit 0.50.2 documentation](https://streamlit.io/docs/api.html#display-text)

## start
```python
text = st.text_area("Text to analyze", DEFAULT_TEXT)

# states is a dict of postal state code to human-readable state name
# e.g. {"CA":"California", "NY":"New York"}, etc.
states = get_states()
state = st.selectbox("State", options=list(states.keys()), format_func=lambda k: states.get(k), )

dot_size = st.slider("Dot size", min_value=1, max_value=20, value=5)
```

## interactive
```python
import streamlit as st
from datetime import time
from datetime import date

st.title("Interactive Widgets")

st.subheader("Checkbox")
w1 = st.checkbox("I am human", True)
st.write(w1)

if w1:
    st.write("Agreed")

st.subheader("Slider")
w2 = st.slider("Age", 0.0, 100.0, (32.5, 72.5), 0.5)
st.write(w2)

st.subheader("Textarea")
w3 = st.text_area("Comments", "Streamlit is awesomeness!")
st.write(w3)

st.subheader("Button")
w4 = st.button("Click me")
st.write(w4)

if w4:
    st.write("Hello, Interactive Streamlit!")

st.subheader("Radio")
options = ("female", "male")
w5 = st.radio("Gender", options, 1)
st.write(w5)

st.subheader("Text input")
w6 = st.text_input("Text input widget", "i iz input")
st.write(w6)

st.subheader("Selectbox")
options = ("first", "second")
w7 = st.selectbox("Options", options, 1)
st.write(w7)

st.subheader("Time Input")
w8 = st.time_input("Set an alarm for", time(8, 45))
st.write(w8)

st.subheader("Date Input")
w9 = st.date_input("A date to celebrate", date(2019, 7, 6))
st.write(w9)

# number input
number = st.number_input('Insert a number')
st.write('The current number is ', number)
```

## lists
```python
lists = [
    [],
    [10, 20, 30],
    [[10, 20, 30], [1, 2, 3]],
    [[10, 20, 30], [1]],
    [[10, "hi", 30], [1]],
    [[{"foo": "bar"}, "hi", 30], [1]],
    [[{"foo": "bar"}, "hi", 30], [1, [100, 200, 300, 400]]],
]


for i, l in enumerate(lists):
    st.header("List %d" % i)

    st.write("With st.write")
    st.write(l)

    st.write("With st.json")
    st.json(l)

    st.write("With st.dataframe")
    st.dataframe(l)
```
