import math
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Vehicle

# Create your views here.

def getPriceTravel(request, latitud_user, longitud_user, latitud_arriv, longitud_arriv):
    
    traveldis = calcular_distancia(float(latitud_user), float(longitud_user), float(latitud_arriv), float(longitud_arriv))
    dict = getNearVehicle(float(latitud_user), float(longitud_user))
    
    vehicle = Vehicle.objects.get(plate = dict['plate'])

    if vehicle.year >= 2010 or vehicle.year < 2015:  
        price = (traveldis * 4) + (dict['distance'])

    elif vehicle.year >= 2015 or vehicle.year < 2020:
        price = (traveldis * 4.5) + (dict['distance'])
    else:
        price = (traveldis * 5.1)+ (dict['distance'])
    
    price_eth = (price/6.92)/obtener_precio_eth()

    return JsonResponse({
        'status_code': 202,
        'precio_bs' : price,
        'precio_eth' : price_eth
    })

   


def getNearVehicle(latitud_user, longitud_user):
    
    distancia_menor = 1000000000000
    placa = ""
    for vehicle in Vehicle.objects.all():
        distancia = calcular_distancia(vehicle.latitud, vehicle.longitud, latitud_user, longitud_user)
        
        if (distancia < distancia_menor):
            distancia_menor = distancia
            placa = vehicle.plate

    return {'plate': placa, 'distance' : distancia_menor}


def calcular_distancia(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radio_tierra = 6371

    # Convertir las latitudes y longitudes a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencia entre las latitudes y longitudes
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Aplicar la fórmula del haversine
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c

    return distancia

def obtener_precio_eth():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    precio = data['ethereum']['usd']
    return precio

def setVehiclestatus(plate, distance):
    vehicle = Vehicle.objects.get(plate = plate)
    vehicle.mileage += distance

    if vehicle.year >= 2010 or vehicle.year < 2015:

        vehicle.batery       -= (distance*100)/338
        vehicle.brake_system -= (distance*100)/20000
        vehicle.suspension   -= (distance*100)/10000
        vehicle.tire_1       -= (distance*100)/40000
        vehicle.tire_2       -= (distance*100)/40000
        vehicle.tire_3       -= (distance*100)/40000
        vehicle.tire_4       -= (distance*100)/40000
        vehicle.cleaning     -= (distance*5)/10 #Cada 10 km se restara un 5 porciento de limpieza 

    elif vehicle.year >= 2015 or vehicle.year < 2020:
        
        vehicle.batery       -= (distance*100)/338
        vehicle.brake_system -= (distance*100)/20000
        vehicle.suspension   -= (distance*100)/10000
        vehicle.tire_1       -= (distance*100)/40000
        vehicle.tire_2       -= (distance*100)/40000
        vehicle.tire_3       -= (distance*100)/40000
        vehicle.tire_4       -= (distance*100)/40000
        vehicle.cleaning     -= (distance*5)/10 #Cada 10 km se restara un 5 porciento de limpieza 

    else:

        vehicle.batery       -= (distance*100)/338
        vehicle.brake_system -= (distance*100)/20000
        vehicle.suspension   -= (distance*100)/10000
        vehicle.tire_1       -= (distance*100)/40000
        vehicle.tire_2       -= (distance*100)/40000
        vehicle.tire_3       -= (distance*100)/40000
        vehicle.tire_4       -= (distance*100)/40000
        vehicle.cleaning     -= (distance*5)/10 #Cada 10 km se restara un 5 porciento de limpieza 

        
    vehicle.save()

    #hacer un if para verificar si algunos niveles de los atributos estan medios o bajos
    #cambiar es estado del auto a Malo o Regular

    return True