
import streamlit as st
import geopandas as gpd
import leafmap.foliumap as lm
import requests
import pandas as pd
import time

api_key = "8a07d886a504428a8e1202226231003"
base_url = "http://api.weatherapi.com/v1/current.json?key=8a07d886a504428a8e1202226231003&q=&aqi=no"
forecast_url = "http://api.weatherapi.com/v1/future.json?key=8a07d886a504428a8e1202226231003&q=&dt=2023-04-09"
map = lm.Map()
# function call wether api using city name, get wether data and add point tp map
def get_current_temperature(link):
     url = base_url + "appid=" + api_key + "&q=" + link
     response = requests.get(url)
     weather_data = response.json()
     st.write(weather_data)
     country = weather_data["location"]['country']
     lat = [weather_data["location"]["lat"]]
     lon = [weather_data["location"]["lon"]]
     localtime = weather_data["location"]["localtime"]
     temp = weather_data['current']['temp_c']
     text = weather_data['current']['condition']['text']
     humidity= weather_data['current']['humidity']
     pressure_mb= weather_data['current']['pressure_mb']
     df = pd.DataFrame(
	{
		'Country': country,
		'temp':temp,
		'humidity':humidity,
		'pressure_mb':pressure_mb,
		"text":text,
		"localtime":localtime,
		'Latitude': lat,
		'Longitude': lon,})
     gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
     gdf = gdf.set_crs('EPSG:4326')
     map.add_gdf(gdf)
def creat_text():
    city = st.text_input("city")
    return get_current_temperature(city)
with st.sidebar:
    st.markdown("<h1 style='color: aqua; text-align: center;'>AS MAP</h1>",unsafe_allow_html=True)
    baseList = st.selectbox("Choose your Basemap",('Open Street Map','Google HYBRID'))
    if baseList == "Open Street Map":
        pass
    else :
         map.add_basemap("HYBRID") 
    cities = st.file_uploader("upload file for heat map",type="geojson")
    if cities:
        gfile = gpd.read_file(cities)
        map.add_gdf(gfile)
    df = gpd.read_file('tr.geojson')
    df_boundry = gpd.read_file('egypt.geojson')
    def style_function(feature):
         return {'fillColor': '#d62b4a', 'fillOpacity': .5, 'weight': 1}
    heat_data = [[row['geometry'].y, row['geometry'].x, row['temperature']] for index, row in df.iterrows()]
    map.add_heatmap(heat_data, name='Temperature Heatmap', radius=40)
    map.add_gdf(df_boundry, style_function=style_function)
    map.add_gdf(df)
   
    city = st.text_input("city")
    if city:
    	get_current_temperature(city)               
map.to_streamlit(hight = 500)

