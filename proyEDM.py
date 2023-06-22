#ric#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import csv
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import datetime
import time
from geopy.geocoders import Nominatim
from time import sleep
import requests
from datetime import datetime, timedelta
from plot_distrib import *

loc = Nominatim(user_agent="GetLoc")

st.set_page_config(page_title="ParkingFinder", layout='wide', initial_sidebar_state = "auto")
data = {'lat': [], 'lon': []}

st.title("Nearest Bike Parking Finder")

#to auto-update components
placeholder = st.empty()

def obtener_tiempo_madrid():
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": "ebbc696950b4436a88a155849232106",
        "q": "Madrid"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def obtener_tiempo_madrid_anterior(fecha):
    url = "http://api.weatherapi.com/v1/history.json"
    params = {
        "key": "ebbc696950b4436a88a155849232106",
        "q": "Madrid",
        "dt": fecha.strftime("%Y-%m-%d"),
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

with placeholder.container():
    # Obtener los datos del tiempo actual de Madrid
    tiempo_madrid = obtener_tiempo_madrid()
    
    # Calcular la fecha del día anterior
    fecha_anterior = datetime.now() - timedelta(days=1)
    
    # Obtener los datos del tiempo del día anterior en Madrid
    tiempo_anterior = obtener_tiempo_madrid_anterior(fecha_anterior)
    
    m1,m2,m3 = st.columns(3, gap = "small")
    m1.metric(label="Temperature", value= "{}°C".format(tiempo_madrid['current']['temp_c']), delta = "{}°C".format(round(tiempo_madrid['current']['temp_c'] - tiempo_anterior['forecast']['forecastday'][0]['day']['avgtemp_c'],1)))
    
    m2.metric(label="Humidity", value= "{}%".format(tiempo_madrid['current']['humidity']), delta = "{}%".format(round(tiempo_madrid['current']['humidity'] - tiempo_anterior['forecast']['forecastday'][0]['day']['avghumidity'],1)))
    
    m3.metric(label= "Conditions", value="{}".format(tiempo_madrid['current']['condition']['text']), delta = "{}".format(tiempo_anterior['forecast']['forecastday'][0]['day']['condition']['text']), delta_color= 'off')

    time.sleep(1)


coord_geo = {"Madrid" : {"lon": -3.7025600, "lat": 40.4165000}}

col1,col2 = st.columns(2)
with col1:
    ciudad = "Madrid"
    destino = st.text_input("Origin", "Ejemplo: Gran Vía")

with col2:
    # Insertar un espacio en blanco para poner "elegir tema" abajo del todo
    df_puntos = {'lat':[], 'lon':[]}
    lista_bicis = pd.read_csv("bicis1.csv", header = 0, sep = ';', encoding='latin-1')
    distrito = []
    for dis in lista_bicis['Distrito']:
        dis_final = dis[4:]
        if dis_final == 'CHAMBERê':
            dis_final = 'CHAMBERÍ'
        if dis_final == 'TETUçN':
            dis_final = 'TETUÁN'
        if dis_final == 'CHAMARTêN':
            dis_final = 'CHAMARTÍN'
        distrito.append(dis_final)
        
        
    if destino != "Eje: Gran Vía":
        def dirToCoord(df, calle):
            minimo = 10000000
            for i in range(len(df)):
                eje_lon = abs(float(df.loc[i,'Longitud'])-calle.longitude)
                eje_lat = abs(float(df.loc[i,'Latitud'])-calle.latitude)
                a = eje_lat + eje_lon
                if a < minimo:
                    minimo = a
                    fila = i
            return fila
        
        if "Madrid, España" not in destino:
            u = destino + ", Madrid, España"
            getLoc_calle = loc.geocode(destino)
            if getLoc_calle:
                row = dirToCoord(lista_bicis, getLoc_calle)
                #a = lista_coords.loc[lista_coords.loc[:,0] == dirToCoord(lista_coords, getLoc_calle)]
                df_puntos['lon'].append(float(lista_bicis.loc[row, 'Longitud']))
                df_puntos['lat'].append(float(lista_bicis.loc[row, 'Latitud']))
                                                                                 
            else:
                pass
        if len(df_puntos['lat']) > 0:
            fig = go.Figure(go.Scattermapbox(
                mode='markers+text',
                name = 'PARKING',
                lat=[df_puntos['lat'][0]],
                lon=[df_puntos['lon'][0]],
                marker = {'size': 9, 'color':'red'},
                    ))
            centered = {'lon' : df_puntos['lon'][0],'lat' : df_puntos['lat'][0]}
            fig.update_layout(mapbox_style="carto-positron", mapbox=dict(center = centered, zoom = 15))
            fig.update_layout(height=800,width=1000) 
            u = lista_bicis.loc[row, 'Calle'] +", Madrid, España"
            
        else: 
            fig = px.scatter_mapbox(df_puntos, lat='lat', lon='lon', center = coord_geo['Madrid'], zoom = 11)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(height=800,width=1000)
    
    
    # Mostrar el mapa interactivo en Streamlit
    st.plotly_chart(fig)

with col1:
    if loc.geocode(u):
        st.write(loc.geocode(u))
    else: pass
    st.write(lista_bicis.loc[row][9])
    st.write(lista_bicis.loc[row, 'Distrito'])
    st.write(distrito)

    with st.expander('Graphics'):
        st.write("The chart above shows the distribution plot of the available slots in the bike's parkings")
        st.distribution_plot(lista_bicis.loc[row, 'Nmero de Plazas'])
    # Mostrar los datos en la página web

    
    
    ################################################################

