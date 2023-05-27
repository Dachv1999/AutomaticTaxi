import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.hashers import check_password

from .models import Person
from .serializers import PersonTokenSerializer

@api_view(['POST'])
def login(request):

    #request.method == 'POST':
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    email = received_json_data['email']
    password = received_json_data['password']

    try: 
        user = Person.objects.get(email=email)
    except Person.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Email Inválido'
        })

    
    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Contraseña Inválida'
        })

    
    token, _ = Token.objects.get_or_create(user=user)
    user_serializer = PersonTokenSerializer(user)
    return Response({
        'status_code': status.HTTP_201_CREATED,
        'msg': 'Votación terminada satisfactoriamente',
        'user': user_serializer.data,
        'token': token.key
    })


@api_view(['POST'])
def logout(request):
    try:
        received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
        token = received_json_data['token']
        token = Token.objects.filter(key=token).first()

        if token:
            token.delete()

            return JsonResponse({
                'status_code': status.HTTP_200_OK,
                'msg': 'Token eliminado'
            })
        
        return JsonResponse({
                'status_code': status.HTTP_400_BAD_REQUEST,
                'msg': 'No se ha encontrado un usuario con esas credenciales'
            })

    except:
        JsonResponse({
                'status_code': status.HTTP_409_CONFLICT,
                'msg': 'No se ha encontrado token en la peticion'
            })
    


