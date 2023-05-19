from .models import Person
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):  #clase para lo que el JSON devolvera
    class Meta:
        model  = Person
        fields = ['ci','name','lastname','date_birth','city','email','password','home','created_at','updated_at','location','is_Admin','id_wallet']
        read_onty_fields = ('created_at', 'updated_at',) #atributos que no podra modificar

""" class CustomerSerializer(serializers.ModelSerializer):  #clase para lo que el JSON devolvera
    class Meta:
        model  = Customer
        fields = ['ci','name','lastname','date_birth','city','email','password','home','created_at','updated_at','location','is_Admin','id_wallet']
        read_onty_fields = ('created_at', 'updated_at',) #atributos que no podra modificar

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Owner
        fields = ['ci','name','lastname','date_birth','city','email','password','home','created_at','updated_at','token','id_enterprise']
        read_onty_fields = ('created_at', 'updated_at',) """