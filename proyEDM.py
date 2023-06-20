#!/usr/bin/env python
# coding: utf-8

# In[1]:



import streamlit as st
import csv
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import datetime
import time
from geopy.geocoders import Nominatim
from time import sleep
loc = Nominatim(user_agent="GetLoc")

st.set_page_config(page_title="ParkingFinder", layout='wide', initial_sidebar_state = "auto")
data = {'lat': [], 'lon': []}

res = {

"tFamilyTTypeTCategory": [ { "poiCategory":["001"], "poiFamily":"001", "poiType":"001" } ],
"longitude":None,
"latitude": None,
"dateTimeUse":None,
"language":"ES",
"minimumPlacesAvailable": [ None ],
"nameFieldCodes": [ { "string":["001"], "nameField":"Tipo plaza" } ],
"radius":50
}


def get_time_of_day():
now = datetime.datetime.now()
hour = now.hour

if hour >= 6 and hour < 19:
    return "carto-positron"
else:
    return "carto-darkmatter"


coord_geo = {"Madrid" : {"lon": -3.7025600, "lat": 40.4165000}}

with st.sidebar:
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.title("SmartRoute")
lista_paradas = []
ciudad = "Madrid"
destino = st.text_input("Destino", "Ejemplo: Gran Vía")

             
                
################################

# Insertar un espacio en blanco para poner "elegir tema" abajo del todo
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
st.markdown("\n")
  

col3, col4= st.columns(2)
with col3:
    if get_time_of_day() == "carto-positron": ind = 0
    else: ind = 1
    theme2 = st.selectbox("Elige el tema", ("Light", "Dark"), index = ind)
    if theme2 == "Light":
        theme = "carto-positron"
    else:
        theme = "carto-darkmatter"


################################################################
df_puntos = {'lat':[], 'lon':[]}
lista_bicis = pd.read_csv("bicis.csv", header = None)
lista_coords = pd.read_csv("coords.csv", header = None)
lista_coords = lista_coords.iloc[:,0:3]
if destino != "Eje: Gran Vía":
def dirToCoord(df, calle):
    minimo = 10000
    for i in range(len(df)):
        eje_lon = abs(df.loc[i,1]-calle.longitude)
        eje_lat = abs(df.loc[i,2]-calle.latitude)
        a = eje_lat + eje_lon
        if a < minimo:
            minimo = a
            fila = i
    return lista_coords.iloc[fila,0]

lista_puntos = []

if "Madrid, España" not in destino:
    destino = destino + ", Madrid, España"
getLoc_calle = loc.geocode(destino)
if getLoc_calle:
        lista_puntos.append(dirToCoord(lista_bicis, getLoc_calle))
        a = lista_bicis.loc[lista_bicis.loc[:,0] == dirToCoord(lista_coords, getLoc_calle)]
        df_puntos['lat'].append(float(a[2].values))
        df_puntos['lon'].append(float(a[1].values))
                                                                     
        else:
            pass
        
fig = px.scatter_mapbox(df_puntos, lat='lat', lon='lon', center = coord_geo["Madrid"], zoom = 11)
fig.update_layout(mapbox_style=theme)
fig.update_layout(height=900,width=1000)



# Mostrar el mapa interactivo en Streamlit
st.plotly_chart(fig)




