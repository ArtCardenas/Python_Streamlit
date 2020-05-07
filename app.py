import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

st.write("# Uber Pickups in New York City")
st.markdown(
"""
This is a demo of a Streamlit app that shows the Uber pickups
geographical distribution in New York City. Use the slider
to pick a specific hour and look at how the charts change.
[See source code](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py)
""")

@st.cache  # keeps data in memory, we can use interactively  (persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)   # load 100,000 records 
# hour = 12
# hour = st.sidebar.slider('hour',0,23,10)
# hour = st.sidebar.number_input('hour',0,23,1)
# st.slider  # displays help
hour = st.slider ('hour',0,23,10)

# select only records where pickup date hour = 12pm;  Note .dt.hour is a function and not a column
data = data[data[DATE_TIME].dt.hour==hour]  

# display the data, I think this is a StreamLit functionality
# 'data',data 


# view a 2D-3D map of the data,  shift key for 3D
'## Geo Data at %sh' % hour
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))


if st.checkbox('Show Raw Data'):
    '## Geo Data at %sh' % hour, data  # displays the comment and the data
