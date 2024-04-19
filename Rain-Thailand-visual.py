import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.express as px

import math

#read data
@st.cache_data
def load_data():
    return pd.read_csv("RainDaily_Tabular.csv")

df = load_data()
# Sidebar
st.sidebar.header('Filter data by date and province')
    
#column date
date = df['date'].unique()
    
#side bar date
option_date_1 = st.sidebar.selectbox(
    'Select start date of data',
    date
)
    

option_date_2 = st.sidebar.selectbox(
    'Select end date of data',
    date,
    index=len(date)-1
)

st.sidebar.write('Date:', option_date_1, ' - ', option_date_2)
    
filter_df = df[(df['date'] >= option_date_1) & (df['date'] <= option_date_2)]

print(filter_df)

#column province
provinces = df['province'].unique()

#side bar province use multi select
option_provinces = st.sidebar.multiselect("Select province", provinces, provinces)

filter_df = filter_df[(filter_df['province'].isin(option_provinces))]

def bar_province(dataframe):

    st.write('### Average of rain by provinces')
    average_rain_by_provinces = (dataframe.groupby(['province'])['rain'].mean())
    st.bar_chart(average_rain_by_provinces)
    
def line_time(datafram):
    st.write('### Average of rain by date')
    
    average_rain_by_province_date = datafram.groupby(["province", "date"])["rain"].mean().round(2).reset_index()
    
    fig = px.line(
        data_frame=average_rain_by_province_date,
        x="date",
        y="rain",
        color="province",
        labels={"rain": "Average of rain", "province": "Province"},
    )
    st.write(fig)
    
def create_map_location(datafram):
    st.write('### Map of average rain by province and date') 
    df_group_by_latitude_longtitude = (
    filter_df.groupby(["latitude", "longitude"])["rain"]
    .sum()
    .round(2)
    .reset_index()
    )
    
    # heat map
    layer = pdk.Layer(
        "HeatmapLayer",
        df_group_by_latitude_longtitude,
        get_position=["longitude", "latitude"],
        get_weight="rain",  
        opacity=0.5,
        pickable=True
    )
    
    view_state = pdk.ViewState(
        longitude=datafram['longitude'].mean(),
        latitude=datafram['latitude'].mean(),
        zoom=5
    )

    return pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v11", tooltip={"text": "{name}\n{address}"})    


def summation(datafram):
    st.write('### Information')
    st.write("Start Date: " , option_date_1)
    st.write("End Date: " ,option_date_2)
    st.write(f"Selected Provinces: {', '.join(option_provinces)}")
    st.write("### Statistic")
    st.write(f"Total Rain: {filter_df['rain'].sum()}")
    st.write(f"Average Rain: {filter_df['rain'].mean()}")
    st.write(f"Median Rain: {filter_df['rain'].median()}")
    st.write(f"Standard Deviation Rain: {filter_df['rain'].std()}")
    st.write(f"Max Rain: {filter_df['rain'].max()}")
    st.write(f"Min Rain: {filter_df['rain'].min()}")
    


# Main app
st.title("Average rain in Thailand")

#bar chart
bar_province(filter_df)

#line chart
line_time(filter_df)

# Display Map
map = create_map_location(filter_df)
st.pydeck_chart(map)

# Display data
st.write('### Datafram') 
st.dataframe(filter_df)

summation(filter_df)

def code():
    st.write('### Source Code')
    st.code("""
        import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.express as px

import math

#read data
@st.cache_data
def load_data():
    return pd.read_csv("RainDaily_Tabular.csv")

df = load_data()
# Sidebar
st.sidebar.header('Filter data by date and province')
    
#column date
date = df['date'].unique()
    
#side bar date
option_date_1 = st.sidebar.selectbox(
    'Select start date of data',
    date
)
    

option_date_2 = st.sidebar.selectbox(
    'Select end date of data',
    date,
    index=len(date)-1
)

st.sidebar.write('Date:', option_date_1, ' - ', option_date_2)
    
filter_df = df[(df['date'] >= option_date_1) & (df['date'] <= option_date_2)]

print(filter_df)

#column province
provinces = df['province'].unique()

#side bar province use multi select
option_provinces = st.sidebar.multiselect("Select province", provinces, provinces)

filter_df = filter_df[(filter_df['province'].isin(option_provinces))]

def bar_province(dataframe):

    st.write('### Average of rain by provinces')
    average_rain_by_provinces = (dataframe.groupby(['province'])['rain'].mean())
    st.bar_chart(average_rain_by_provinces)
    
def line_time(datafram):
    st.write('### Average of rain by date')
    
    average_rain_by_province_date = datafram.groupby(["province", "date"])["rain"].mean().round(2).reset_index()
    
    fig = px.line(
        data_frame=average_rain_by_province_date,
        x="date",
        y="rain",
        color="province",
        labels={"rain": "Average of rain", "province": "Province"},
    )
    st.write(fig)
    
def create_map_location(datafram):
    st.write('### Map of average rain by province and date') 
    df_group_by_latitude_longtitude = (
    filter_df.groupby(["latitude", "longitude"])["rain"]
    .sum()
    .round(2)
    .reset_index()
    )
    
    # heat map
    layer = pdk.Layer(
        "HeatmapLayer",
        df_group_by_latitude_longtitude,
        get_position=["longitude", "latitude"],
        get_weight="rain",  
        opacity=0.5,
        pickable=True
    )
    
    view_state = pdk.ViewState(
        longitude=datafram['longitude'].mean(),
        latitude=datafram['latitude'].mean(),
        zoom=5
    )

    return pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v11", tooltip={"text": "{name}\n{address}"})    


def summation(datafram):
    st.write('### Information')
    st.write("Start Date: " , option_date_1)
    st.write("End Date: " ,option_date_2)
    st.write(f"Selected Provinces: {', '.join(option_provinces)}")
    st.write("### Statistic")
    st.write(f"Total Rain: {filter_df['rain'].sum()}")
    st.write(f"Average Rain: {filter_df['rain'].mean()}")
    st.write(f"Median Rain: {filter_df['rain'].median()}")
    st.write(f"Standard Deviation Rain: {filter_df['rain'].std()}")
    st.write(f"Max Rain: {filter_df['rain'].max()}")
    st.write(f"Min Rain: {filter_df['rain'].min()}")
    


# Main app
st.title("Average rain in Thailand")

#bar chart
bar_province(filter_df)

#line chart
line_time(filter_df)

# Display Map
map = create_map_location(filter_df)
st.pydeck_chart(map)

# Display data
st.write('### Datafram') 
st.dataframe(filter_df)

summation(filter_df)

            """)
code()