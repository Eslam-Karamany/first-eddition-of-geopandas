import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap

# Read the temperature data
df = gpd.read_file('tr.geojson')

# Read the Egypt boundary data
df_boundry = gpd.read_file('egypt.geojson')

# Define a style function to fill the polygons with a color
def style_function(feature):
    return {'fillColor': '#d62b4a', 'fillOpacity': .5, 'weight': 1}

# Create a Leafmap map object
m = leafmap.Map()

# Add the heatmap layer to the map
heat_data = [[row['geometry'].y, row['geometry'].x, row['temperature']] for index, row in df.iterrows()]
m.add_heatmap(heat_data, name='Temperature Heatmap', radius=40)

# Add the Egypt boundary to the map with the style function
m.add_gdf(df_boundry, style_function=style_function)

# Add the temperature data to the map
m.add_gdf(df)

# Display the map
m.to_streamlit(height=500)



######################################################################################################


# import pandas as pd
# import geopandas as gpd
# import streamlit as st

# df = pd.DataFrame(
#     {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
#      'Temp': ['23', '25', '27', '32', '34'],
#      'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
#      'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})

# gdf = gpd.GeoDataFrame(
#     df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# # Rename the 'Latitude' and 'Longitude' columns to 'lat' and 'lon'
# gdf = gdf.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

#############################################################################







# ############################################################################################


# import streamlit as st
# import geopandas as gpd



# # Load data from GeoJSON file using geopandas
# geojson_file = "xyss.geojson"
# data = gpd.read_file(geojson_file)
# data=data.set_crs("EPSG:4326")

# # Extract latitude and longitude columns from geometry
# data['lon'] = data.geometry.x
# data['lat'] = data.geometry.y

# # Drop the geometry column
# data = data.drop(columns=['geometry'])

# # Display data on map using Streamlit
# st.map(data)



# __________________________________________________________________________-

# import geopandas as gpd
# import streamlit as st
# import matplotlib.pyplot as plt
# import requests
# import leafmap.foliumap as leafmap



# # headers = {
# #     'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
# # }

# df = gpd.read_file('FF.geojson')
# df = df.to_crs(epsg=4326)
# m=leafmap.Map()
# m.add_gdf(df)
# m.to_streamlit(height=500)







# inputFile = st.file_uploader("upload file",type="geojson")
# if  inputFile:
#     call = requests.get('https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248651833fc5a5c43a3b3920e683a135c1a&start=30.9853,30.0853&end=31.0444,30.0882', headers=headers)
#     df =gpd.read_file(call.text)
#     gfile = gpd.read_file(inputFile).to_crs('EPSG:3857')
#     # fig, ax = plt.subplots(figsize=(10, 10))
#     # gfile.plot(column='OZONE', cmap='YlOrRd', ax=ax, linewidth=0.1, edgecolor='black', legend=True)
#     # plt.show()
#     m = leafmap.Map()
#     gfile.plot()
#     m.add_gdf(gfile)
#     m.add_gdf(df)

#     m.to_streamlit(height=500)