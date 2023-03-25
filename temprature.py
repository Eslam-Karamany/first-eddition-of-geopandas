import streamlit as st
import geopandas as gpd
import leafmap.foliumap as lm
import requests
import pandas as pd
import matplotlib.pyplot as plt


map = lm.Map(max_zoom=7)

api_key = "8a07d886a504428a8e1202226231003"
base_url = "http://api.weatherapi.com/v1/current.json?key=" + api_key + "&q="
forecast_url = "http://api.weatherapi.com/v1/future.json?key=" + api_key + "&q=&dt=2023-04-09"


st.set_page_config(page_title="Wether App", page_icon=":cloud:", layout="wide")


def get_current_temperature(city):
    url = base_url + city
    response = requests.get(url)
    weather_data = response.json()

    country = weather_data["location"]["country"]
    lat = weather_data["location"]["lat"]
    lon = weather_data["location"]["lon"]
    localtime = weather_data["location"]["localtime"]
    temp = weather_data["current"]["temp_c"]
    text = weather_data["current"]["condition"]["text"]
    humidity = weather_data["current"]["humidity"]
    pressure_mb = weather_data["current"]["pressure_mb"]

    df = pd.DataFrame({
        "Country": [country],
        "Temperature (°C)": [temp],
        "Humidity (%)": [humidity],
        "Pressure (mb)": [pressure_mb],
        "Weather Condition": [text],
        "Local Time": [localtime],
        "Latitude": [lat],
        "Longitude": [lon],
    })


    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    gdf = gdf.set_crs("EPSG:4326")
    map.add_gdf(gdf)
    map.set_center(lon,lat)

def addAttributesOptions(gfile):
    # atts = gfile.columns
    # tuAtts = tuple(" ")+tuple(atts)
    attList = st.selectbox("choose the value column",("temprature","humadity"))
    if not attList == " ":
        lat = gfile.geometry.y
        long = gfile.geometry.x
        value = gfile[attList]
        length = len(lat)
        data = []
        for i in range(0,length):
            point = [lat[i],long[i],float(value[i])]
            data.append(point)
        map.add_heatmap(data)

        

with st.sidebar:
    st.sidebar.empty()
with st.sidebar:
    st.sidebar.markdown("<h2 style='color: white; font-size: 16px; text-align: center;'>User guide</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: gray; font-size: 14px; text-align: center;'>You can use the application to search any city.</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: gray; font-size: 14px; text-align: center;'>When you hover over a city, a live info will pop up.</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: gray; font-size: 14px; text-align: center;'>You can import the `egypt_cities.geojson` file and choose the field to draw with.</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: aqua; text-align: center;'>Weather MAP</h1>", unsafe_allow_html=True)

    baseList = st.selectbox("Choose your Basemap", ("Open Street Map", "Google HYBRID"))
    if baseList == "Open Street Map":
        pass
    else:
        map.add_basemap("HYBRID") 

    city = st.text_input("Enter a city name:")
    if city:
        get_current_temperature(city)




    cities = st.file_uploader("Upload a GeoJSON file for the heatmap", type="geojson")

    if cities:
        gfile = gpd.read_file(cities)
        heat_data = [[row["geometry"].y, row["geometry"].x, row["temprature"]] for index, row in gfile.iterrows()]
        addAttributesOptions(gfile)
            
        if not city or cities:
            map.set_center(31.,30.0444,zoom=6)



map.to_streamlit(height=500)

