# https://twitter.com/agarcia_me/status/1183868561149722626
# https://glitch.com/edit/#!/hello-streamlit?path=app.py:203:3
import streamlit as st
import pandas as pd
import urllib.request
import json

from delegates.geo_helper import get_states

fetch_csv = st.cache(pd.read_csv)
fetch_json = st.cache(pd.read_json)

"""
# Hello, world!

This is an example [`streamlit`](https://streamlit.io/) app running on [Glitch](https://glitch.com/).

This Glitch app install streamlit, and does a `streamlit run app.py` on port 3000 to start the app. You can edit `app.py` (where this code lies) to test this out!

"""

"""
--- 


## Streamlit Playground

"""

with st.echo():
    print("You can see this code! 😮")

st.json({
    'foo': 'bar',
    'baz': 'boz',
    'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],
})

st.graphviz_chart('''
  digraph {
    rankdir=LR;
    a -> c;
    b -> c;
    c -> d;
    d -> e;
    d -> f;
    f -> g;
  }''')

if st.button("balloon me"):
    st.balloons()

"""
---

## Opioid Sales

Source: Washington Posts's [ARCOS API](https://arcos-api.ext.nile.works/__swagger__/) - Original article [here](https://www.washingtonpost.com/graphics/2019/investigations/dea-pain-pill-database/)

"""

# states is a dict of postal state code to human-readable state name
# e.g. {"CA":"California", "NY":"New York"}, etc.
states = get_states()

state = st.selectbox("State", options=list(states.keys()), format_func=lambda k: states.get(k), )

# raw_pharmacy_data = fetch_json(
#     "https://arcos-api.ext.nile.works/v1/total_pharmacies_state?state={state}&key=WaPo".format(state=state))

## only state==CA
raw_pharmacy_data = fetch_json('/pi/ai/streamlit/total_pharmacies_state.json')

st.markdown("""### Opioid Sales in {state}


""".format(state=states.get(state)))

raw_pharmacy_data

st.vega_lite_chart(raw_pharmacy_data, {
    'mark': 'bar',
    'encoding': {
        'x': {'field': 'buyer_county', 'type': 'nominal', "sort": "y"},
        'y': {'field': 'total_dosage_unit', 'type': 'quantitative', 'aggregate': 'sum'}
    },
}, height=1000)

"**Note**: there seems to be a bug with vegalite in Streamlit where the height is fixed at 200px... I might be wrong about this, but I'll file a bug report if I can't fix it"

"""
---

## Apple Stock Price 2007-2012

Source: Mike Bostock [https://observablehq.com/@mbostock/vega-lite-line-chart](https://observablehq.com/@mbostock/vega-lite-line-chart)

"""

# aapl = fetch_csv(
#     'https://gist.githubusercontent.com/mbostock/14613fb82f32f40119009c94f5a46d72/raw/d0d70ffb7b749714e4ba1dece761f6502b2bdea2/aapl.csv')
aapl = fetch_csv('/pi/ai/streamlit/aapl.csv')

aapl

st.vega_lite_chart(aapl, {
    'mark': "line",
    'encoding': {
        'x': {'field': 'date', 'type': 'temporal'},
        'y': {'field': 'close', 'type': 'quantitative'},
    },
}, height=1000)

"""
---

## High Schools in Los Angeles

Source: Los Angeles Times [highschool-homicide-analysis
](https://github.com/datadesk/highschool-homicide-analysis)

"""

# raw_la_schools = fetch_csv(
#     "https://github.com/datadesk/highschool-homicide-analysis/raw/master/output/la-high-schools.csv")
raw_la_schools = fetch_csv('/pi/ai/streamlit/la-high-schools.csv')

map_df = pd.DataFrame()
map_df["lat"] = raw_la_schools["Latitude"]
map_df["lon"] = raw_la_schools["Longitude"]

dot_size = st.slider("Dot size", min_value=1, max_value=20, value=5)

st.deck_gl_chart(viewport={
    'latitude': 33.94,
    'longitude': -118.18,
    'zoom': 10,
    'pitch': 50,
},
    layers=[{
        'data': map_df,
        'radiusScale': dot_size,
        'type': 'ScatterplotLayer'
    }])
st.write("Dot size: ", dot_size)

"""
---

## How to use this Glitch app

You can remix the Glitch project and you'll have your own project running streamlit.  

"""

"""

---

## Limitations

There are some limitations to Glitch, [for example](https://glitch.com/help/restrictions/):

>Projects sleep after 5 minutes if they are not used

> Projects have a limit of 200MB of disk space in the container

(and installing `streamlit` already takes up ~180MB, it seems like)

> Projects have a limit of 512MB of RAM.

> Projects are limited to 4000 requests per hour 


A few other points to consider:

- There's no GPU access, so you probably can't do a ton of crazy ML/AI stuff.

- Glitch autosaves your work while you are typing - which means, when you're editing your streamlit app, it will continuously restart over and over again while you're coding - which is a little annoying... You can turn off auto-run to avoid this

- Glitch uses Python 3.5 (as of now), so some Altair charts [may not render correctly](https://github.com/altair-viz/altair/issues/972) (which is what `st.line_chart` and `st.bar_chart` uses under the hood)

But hey, it's free, you can use this to do quick tests, and it requires no setup!



"""
