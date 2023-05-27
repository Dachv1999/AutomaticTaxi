import math
import json
import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from .models import Vehicle

from ManageEnterprise.models import Enterprise, Invoice
from ManageEnterprise.serializers import InvoiceSerializer


@api_view(['GET'])
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
        'status_code': status.HTTP_200_OK,
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

@api_view(['GET'])
def endTravelplate(plate, distance):
    #En front se debe pagar el viaje
    setVehiclestatus(plate, distance)#actualizar datos segun el recorrido hecho
    fail_list = checkVehicleStatus(plate) #obtenemos una lsta de errores, por si tenemos que enviar al taller algo

    if len(fail_list) > 0:
        return sendToTechnician(fail_list, plate)
    
    return Response({
        'status_code': status.HTTP_200_OK,
        'msg': 'Viaje terminado'
    })



def setVehiclestatus(plate, distance):
    vehicle = Vehicle.objects.get(plate = plate)
    vehicle.mileage += distance

    if vehicle.model == "Tesla Model X":

        vehicle.batery -= (distance*100)/547   #km de resistencia por cada uno de los atributos 
        vehicle.tire_1 -= (distance*100)/40000
        vehicle.tire_2 -= (distance*100)/40000
        vehicle.tire_3 -= (distance*100)/40000
        vehicle.tire_4 -= (distance*100)/40000

    elif vehicle.model == "Tesla Model 3":
        
        vehicle.batery -= (distance*100)/507    
        vehicle.tire_1 -= (distance*100)/50000
        vehicle.tire_2 -= (distance*100)/50000
        vehicle.tire_3 -= (distance*100)/50000
        vehicle.tire_4 -= (distance*100)/50000

    else:

        vehicle.batery -= (distance*100)/525
        vehicle.tire_1 -= (distance*100)/60000
        vehicle.tire_2 -= (distance*100)/60000
        vehicle.tire_3 -= (distance*100)/60000
        vehicle.tire_4 -= (distance*100)/60000
         

    vehicle.brake_system -= (distance*100)/20000
    vehicle.suspension   -= (distance*100)/10000
    vehicle.cleaning     -= (distance*5)/10 #Cada 10 km se restara un 5 porciento de limpieza
    vehicle.save()


    
def checkVehicleStatus(plate):
    vehicle = Vehicle.objects.get(plate = plate)
    fails_list = []
    if vehicle.batery < 10:
        fails_list.append("Batery low")
    
    if vehicle.tire_1 < 5:
        fails_list.append("Flat tire")

    if vehicle.break_system < 8:
        fails_list.append("Brake failure")

    if vehicle.suspension < 5:
        fails_list.append("Suspension failure")

    if vehicle.cleaning < 20:
        fails_list.append("Dirty vehicle")

    return fails_list
    
def sendToTechnician(fail_list, plate):
    vehicle = Vehicle.objects.get(plate = plate)
    vehicle.is_free = False
    vehicle.save()

    aux = price = 0

    invoice = Invoice()
    invoice.nit = "cuenta harcodeada"
    invoice.id_empresa = Enterprise.objects.get(id = 1)
    
    for error in fail_list:
        if error == "Batery low":
            aux = (100 - vehicle.batery)*0,66  #0,66 Bs vale el KWH en Bolivia
            price += aux
        if error == "Flat tire":
            aux =  (20*4)  #20bs por llanta inflada con nitrogeno
            price += aux
        if error == "Brake failure":
            aux =  3500   #500$ costo promedio de arreglar en sistema de frenos
            price += aux
        if error == "Suspension failure":
            aux =  7000   #1000$ costo promedio de arreglar el sistema de suspension
            price += aux
        if error == "Dirty vehicle":
            aux =  140   #20$ costo promedio de lavado
            price += aux

        invoice.service_desc += error +": "+ str(aux) + "Bs.\n"

    invoice.price = price
    price_eth = (price/6.92)/obtener_precio_eth()    

    invoice.save()
    
    invoice_serializer = InvoiceSerializer(invoice)

    return Response({
        'status_code': status.HTTP_201_CREATED,
        'msg': 'Factura por confirmar',
        'invoice': invoice_serializer.data,
        'price_eth': price_eth
    })
    

@api_view(['GET'])
def repairFails(id_invoice, plate):

    vehicle = Vehicle.objects.get(plate = plate)
    vehicle.is_free = True
    #arreglar todo lo qe esta en la factura
    vehicle.save()

    invoice = Invoice.objects.get(id = id_invoice)
    invoice.is_pay = True
    invoice.save()

    #Pagar y ejecutar smart contract

    return Response({
        'status_code': status.HTTP_202_ACCEPTED,
        'msg': 'Vehiculo reparado'
    })
