import json
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .models import Person

@api_view(['POST'])
def login(request):

    #request.method == 'POST':
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    email = received_json_data['email']
    password = received_json_data['password']

    try: 
        user = Person.objects.get(email=email)
    except Person.DoesNotExist:
        return Response("Email inválido")
    
    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return Response("Contraseña inválida")
    
    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({
        'status_code': 202,
        'msg': 'Votación terminada satisfactoriamente',
        'token': token.key
    })


""" @api_view(['GET'])
def logout(request, ci_user):

    #request.method == 'POST':
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    email = received_json_data['email']
    password = received_json_data['password']

    try: 
        user = Person.objects.get(ci=ci_user)
    except Person.DoesNotExist:
        return Response("Usuario no existe")

    user.

    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return Response("Contraseña inválida")
    
    token, _ = Token.objects.get_or_create(user=user)

    return Response(token.key) """
    


