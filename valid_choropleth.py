import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium


APP_TITLE = 'Streamlit Dashboard'
APP_TITLE1 = 'Welcome to our Dashboard !'
APP_SUB_TITLE = 'Bahtit & Bamessaoud'

st.set_page_config(APP_TITLE)
st.title(APP_TITLE1)
st.caption(APP_SUB_TITLE)


def display_time_filters():
    attribut = st.sidebar.selectbox('Attribut', ["Humidity", "Precipitation", "Temperature"])
    jour = st.sidebar.radio('Quarter', [1, 2, 3, 4, 5, 6, 7])
    st.header(f'{attribut} J{jour}')
    return attribut, jour


def display_map(df, attribut, jour):
    attributJ = attribut + str(jour)
    df[attributJ] = pd.to_numeric(df[attributJ], errors='coerce')
    communes = 'data/communes.geojson'
    m = folium.Map(location=[30, -7.5], zoom_start=5, tiles="cartodbpositron")

    if attribut == 'Humidity':
        fill_color = "Purples"
        unit ='%'
    elif attribut == 'Precipitation':
        fill_color = "Blues"
        unit ='%'
    elif attribut == 'Temperature':
        fill_color = "YlOrRd"
        unit ='°C'

    choropleth = folium.Choropleth(
        geo_data=communes,
        data=df,
        name='Communes du Maroc',
        columns=['commune', attributJ],
        key_on='feature.properties.commune',
        fill_color=fill_color,
        line_opacity=0.6,
        highlight=True
    )
    choropleth.geojson.add_to(m)

    #Tooltip
    df_indexed = df.set_index('commune')
    for feature in choropleth.geojson.data['features']:
        commune = feature['properties']['commune']
        feature['properties'][attributJ] = f'{attribut}: {df_indexed.loc[commune, attributJ]}{unit}'

        
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['commune', attributJ], labels=False))
    
    folium.LayerControl(autoZIndex=False).add_to(m)  
    st_map = st_folium(m, width=600, height=500)
    return st_map


df_meteo = gpd.read_parquet('data/file.parquet')
# Display Filters and Map
attribut, jour = display_time_filters()
display_map(df_meteo, attribut, jour)
