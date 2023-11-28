import streamlit as st
import numpy as np
import geopandas as gpd
from datetime import datetime , timedelta
import random




st.set_page_config('Streamlit Dashboard', layout="wide")
st.title('Welcome to our Dashboard !')
st.caption('Bahtit & Bamessaoud')
  

communes=gpd.read_file("data/centroides.geojson")
geodata = gpd.GeoDataFrame(communes)
gdf = gpd.GeoDataFrame(geometry=geodata['geometry'], crs='EPSG:4326')
gdf['commune'] =geodata['commune']
gdf['Births']= np.random.randint(1, 10, size=len(gdf))
gdf['Deaths']= np.random.randint(1, 10, size=len(gdf))
start_date=datetime(2023,11,1)
end_date=datetime(2023,11,7)
date_range= end_date - start_date
gdf['Date']= [start_date + timedelta(days=random.randint(0,date_range.days)) for _ in range(len(gdf))]
attribut=["Humidity" ,"Precipitation", "Temperature"]
for j in range(3):
    for k in range(1,8):
        attributJ = attribut[j]+str(k)
        if attribut[j] == 'Humidity':
            gdf[attributJ] =np.random.randint(0, 100, size=len(gdf))
        elif attribut[j] == 'Precipitation':
            gdf[attributJ] =np.random.randint(0, 20, size=len(gdf))
        elif attribut[j] == 'Temperature':
            gdf[attributJ] =np.random.randint(0, 50, size=len(gdf))
        

st.write(gdf)
