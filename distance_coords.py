import math

def calcular_distancia(lat1, lon1, lat2, lon2):

    radio_tierra = 6371000


    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)


    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    
    a = math.sin(delta_lat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c

    return distancia
