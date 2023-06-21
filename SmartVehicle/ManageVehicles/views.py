import math
import json
import requests
import pytz
from django.shortcuts import render
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta



from .models import Vehicle, Transaction
from .serializers import TransactionSerializer, AllTransactionSerializer
from ManageEnterprise.models import Enterprise, Invoice
from ManageCounts.models import Person
from ManageEnterprise.serializers import InvoiceSerializer
import random

@api_view(['POST'])
def startTravel(request):
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    plate          = received_json_data['plate_vehicle']
    id_customer    = received_json_data['id_customer']
    type           = received_json_data['type']
    departure_lat  = received_json_data['departure_lat']
    departure_lng  = received_json_data['departure_lng']
    arrival_lat    = received_json_data['arrival_lat']
    arrival_lng    = received_json_data['arrival_lng']
    #departure_time = received_json_data['departure_time']
    travel_time    = received_json_data['travelTime']
    distance       = received_json_data['distance']
    price          = received_json_data['price']

    try: 
        vehicle = Vehicle.objects.get(plate = plate)
    except Vehicle.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Vehiculo no existe'
        })
    
    if vehicle.is_free == False:
        return Response({
        'status_code': status.HTTP_400_BAD_REQUEST,
        'msg': 'El vehiculo esta ocupado'
    })

    try: 
        person = Person.objects.get(ci = id_customer)
    except Person.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Usuario no existe'
        })

    # Obtén el objeto datetime actual con el timezone deseado
    timezone = pytz.timezone('America/La_Paz')
    dt = datetime.now(timezone)

    arrivalTime = dt + timedelta(minutes=int(travel_time)/60)

    transaction = Transaction()
    transaction.plate_vehicle = vehicle
    transaction.customer = person
    transaction.travel_type = type
    transaction.departure_place_lat = departure_lat
    transaction.departure_place_long = departure_lng
    transaction.arrival_place_lat = arrival_lat
    transaction.arrival_place_long = arrival_lng
    transaction.departure_time = dt
    transaction.arrival_time = arrivalTime
    transaction.distance = distance/1000
    transaction.price = price
    transaction.save()

    

    vehicle.is_free = False
    vehicle.save()

    return Response({
        'status_code': status.HTTP_201_CREATED,
        'msg': 'Transaction creada'
    })

@api_view(['GET'])
def getPriceTravel(request, latitud_user, longitud_user, traveldis):
    
    traveldis /= 1000
    print("entra")
    dict = getNearVehicle(float(latitud_user), float(longitud_user))
    
    vehicle = Vehicle.objects.get(plate = dict['plate'])

    if vehicle.model == "Tesla Model X":  
        price = (traveldis * 4) + (dict['distance'])

    elif vehicle.model == "Tesla Model 3":
        price = (traveldis * 4.5) + (dict['distance'])
    else:
        price = (traveldis * 5.1)+ (dict['distance'])
    
    price_eth = (price/6.92)/obtener_precio_eth()

    return JsonResponse({
        'status_code': status.HTTP_200_OK,
        'precio_bs' : round(price, 1),
        'precio_eth' : round(price_eth,5),
        'plate' : vehicle.plate,
        'model' : vehicle.model
    })


def getNearVehicle(latitud_user, longitud_user):
    
    distancia_menor = 1000000000000
    placa = ""
    for vehicle in Vehicle.objects.all():
        distancia = calcular_distancia(vehicle.latitud, vehicle.longitud, latitud_user, longitud_user)
        
        if (distancia < distancia_menor) and (vehicle.is_free != False):
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

@api_view(['POST'])
def endTravelplate(request):
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    plate = received_json_data['plate']
    distance = received_json_data['distance']
    #En front se debe pagar el viaje
    setVehiclestatus(plate, distance)#actualizar datos segun el recorrido hecho
    fail_list = checkVehicleStatus(plate) #obtenemos una lsta de errores, por si tenemos que enviar al taller algo

    if len(fail_list) > 0:
        return sendToTechnician(fail_list, plate)
    
    print(fail_list)
    return Response({
        'status_code': status.HTTP_200_OK,
        'msg': 'Viaje terminado'
    })



def setVehiclestatus(plate, distance):
    vehicle = Vehicle.objects.get(plate = plate)

    try: 
        vehicle = Vehicle.objects.get(plate = plate)
    except Vehicle.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Vehiculo no existe'
        })
    
    distance /= 1000
    vehicle.mileage += distance
    vehicle.is_free = True

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

    if vehicle.brake_system < 8:
        fails_list.append("Brake failure")

    if vehicle.suspension < 5:
        fails_list.append("Suspension failure")

    if vehicle.cleaning < 20:
        fails_list.append("Dirty vehicle")

    return fails_list
    
def sendToTechnician(fail_list, plate):
    vehicle = Vehicle.objects.get(plate = plate)
    vehicle.is_free = False
    vehicle.vehicle_state = 'R'
    vehicle.save()

    aux = 0
    price = 0

    invoice = Invoice()
    invoice.nit = "cuenta harcodeada"
    invoice.id_empresa = Enterprise.objects.get(id = 1)
    
    for error in fail_list:
        if error == "Batery low":
            aux = (100 - vehicle.batery)*0.66  #0,66 Bs vale el KWH en Bolivia
            price += int(aux)
        if error == "Flat tire":
            aux =  (20*4)  #20bs por llanta inflada con nitrogeno
            price += int(aux)
        if error == "Brake failure":
            aux =  3500   #500$ costo promedio de arreglar en sistema de frenos
            price += int(aux)
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
    

@api_view(['POST'])
def repairFails(request):

    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    id_invoice = received_json_data['id_invoice']
    plate = received_json_data['plate']

    try: 
        vehicle = Vehicle.objects.get(plate = plate)
    except Vehicle.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Vehiculo no existe'
        })
    
    try:
        invoice = Invoice.objects.get(id = id_invoice)
    except Invoice.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Factura no encontrada'
        })



    if "Batery low" in invoice.service_desc:
        vehicle.batery = 100
    if "Flat tire" in invoice.service_desc:
        vehicle.tire_1 = 100 
        vehicle.tire_2 = 100
        vehicle.tire_3 = 100
        vehicle.tire_4 = 100
    if "Brake failure" in invoice.service_desc:
        vehicle.brake_system = 100
    if "Suspension failure" in invoice.service_desc:
        vehicle.suspension = 100
    if "Dirty vehicle" in invoice.service_desc:
        vehicle.cleaning = 100

    vehicle.is_free = True
    vehicle.vehicle_state = 'B'
    invoice.is_pay = True
    vehicle.save()
    invoice.save()

    price_eth = (invoice.price/6.92)/obtener_precio_eth()  
    execute_smartContract(price_eth)
    return Response({
        'status_code': status.HTTP_202_ACCEPTED,
        'msg': 'Vehiculo reparado'
    })

def execute_smartContract(price):
    from web3 import Web3
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  # Cambia esta URL si tu instancia de Ganache utiliza un puerto diferente
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # Cargar la dirección y la clave privada del propietario de la cuenta
    owner_address = "0xeCb3Dfb32B40810c72D07B49F63973E860Ac93A8"
    owner_private_key = "07bd57ff34d1f7eeff9d1e8edc9a4060a77f38ec38635c44df1a4feb3732bc97"


    # Cargar el contrato Solidity
    contract_address = "0x2b96108C8CF861F47aBbfD47AfD44b9b7320eE79"
    contract_abi =[
	  {
		"inputs": [],
		"name": "Transaction",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "payable",
		"type": "function"
	   } 
      ]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    #print (contract)
    # Cantidad de ethers a enviar (en wei)
    cantidad_wei = web3.to_wei(price, 'ether')


    # Crear una transacción para llamar a la función del contrato
    transaccion = contract.functions.Transaction().build_transaction({"gasPrice": web3.eth.gas_price,'from': owner_address, 'nonce': web3.eth.get_transaction_count(owner_address), 'value': cantidad_wei})

    #print(transaccion)

    # Firmar y enviar la transacción
    signed_txn = web3.eth.account.sign_transaction(transaccion, private_key=owner_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Esperar a que la transacción se confirme
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transacción confirmada:", tx_receipt) 


@api_view(['GET'])
def getAllTransaction(request, ci_user):
    

    transactions = Transaction.objects.filter(customer=ci_user).order_by('-created_at')
    formato_deseado = "%Y-%m-%d %H:%M"

    for transaction in transactions:
        transaction.departure_time = transaction.departure_time.strftime(formato_deseado)
        transaction.arrival_time = transaction.arrival_time.strftime(formato_deseado)


    serializedData = TransactionSerializer(transactions, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'transactions': serializedData.data
    })

@api_view(['GET'])
def update_locations_randomly(request):

    latitude_list = [-17.394463,-17.387392,-17.384231,-17.393765,-17.392677,-17.380754,
                     -17.372584,-17.373146,-17.378830, -17.381868, -17.365388, -17.367477,
                     -17.393857, -17.392563, -17.391498, -17.390653, -17.393213,-17.395048,
                     -17.369676, -17.413872, -17.401449, -17.401948, -17.362938, -17.419227, -17.375818]
    


    longitude_list = [-66.149372, -66.148576,-66.158697, -66.156453, -66.158771, -66.151099,
                      -66.162411, -66.149523, -66.142153,-66.118970, -66.160225, -66.148327, 
                      -66.181945, -66.205707, -66.230271, -66.243657, -66.273251,-66.280533 ,
                      -66.170389,  -66.178664, -66.175339, -66.157743, -66.147685, -66.131226, -66.151171 ]
    
    vehicules = Vehicle.objects.all()
    m = len(latitude_list )
    list_aux = []
    
    for vehicule in vehicules:
       bandera = True
       #Controlamos que el index no se repita
       while(bandera):
    
           index = congruential_mix(m)
   
           if index not in list_aux:
               #Si no se repite guardamos
               vehicule.latitud = latitude_list[index]
               vehicule.longitud = longitude_list[index]
               vehicule.save()
               list_aux.append(index)
               bandera = False

    return Response({
        'status_code': status.HTTP_202_ACCEPTED,
        'msg': 'Locations Updated'
    })



 
def congruential_mix(m):
    seed = random.randint(0, 200) 
    a = random.randint(1, 50)   
    c = random.randint(1, 50)
   
    result = (a * seed + c) % m
    return result
