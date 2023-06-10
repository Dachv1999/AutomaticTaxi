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

from django.core.validators import validate_email, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

from .models import Person
from .serializers import PersonTokenSerializer, PersonSerializer

@api_view(['POST'])
def register(request):
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON

    ci           = received_json_data['ci']
    name         = received_json_data['name']
    lastname     = received_json_data['lastname']
    city         = received_json_data['city']
    email        = received_json_data['email']
    password     = received_json_data['password']
    is_superuser = received_json_data['is_superuser']
    latitud      = received_json_data['latitud']
    longitud     = received_json_data['longitud']

    if validate_email_format(email) == False:
        return Response({
            'status': status.HTTP_406_NOT_ACCEPTABLE,
            'msg': 'Formato de email inválido'
        })
    
    if personExistByEmail(email):
        return Response({
            'status': status.HTTP_409_CONFLICT,
            'msg': 'Email existnte'
        })

    if personExistByCi(ci):
        return Response({
            'status': status.HTTP_409_CONFLICT,
            'msg': 'CI existente'
        })
    

    if validate_password_format(password) == False:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'msg': 'Contraseña invalida'
        })

    user = Person()

    user.ci = ci
    user.name = name
    user.lastname = lastname
    user.city = city
    user.email = email
    user.set_password(password)
    user.is_superuser = is_superuser
    user.latitud = latitud
    user.longitud = longitud

    user.save()

    user_serializer = PersonSerializer(user)

    return Response({
        'status_code': status.HTTP_201_CREATED,
        'msg': 'Usuario creado',
        'user': user_serializer.data
    })

def validate_email_format(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validate_password_format(password):
    validators = [
        MinLengthValidator(8, message='La contraseña debe tener al menos 8 caracteres.'),
        MaxLengthValidator(20, message='La contraseña no puede exceder los 20 caracteres.'),
        RegexValidator(r'^[a-zA-Z0-9_]*$', message='La contraseña solo puede contener letras, números y guiones bajos (_).'),
    ]

    for validator in validators:
        try:
            validator(password)
        except ValidationError:
            return False

    return True

def personExistByEmail(email):
    try:
        Person.objects.get(email = email)
        return True
    except:
        return False
    
def personExistByCi(ci):
    try:
        Person.objects.get(ci = ci)
        return True
    except:
        return False

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
        'msg': 'Inicio de Sesión satisfactoriamente',
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
    


