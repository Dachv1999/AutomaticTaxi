from .models import Wallet, Customer, Owner
from rest_framework import serializers

class WalletSerializer(serializers.ModelSerializer): #clase para lo que el JSON devolvera
    class Meta:
        model  = Wallet
        fields = ['id','code','money']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = ['ci','name','lastname','date_birth','city','email','password','home','created_at','updated_at','location','is_Admin','id_wallet']
        read_onty_fields = ('created_at', 'updated_at',) #atributos que no podra modificar

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Owner
        fields = ['ci','name','lastname','date_birth','city','email','password','home','created_at','updated_at','token','id_enterprise']
        read_onty_fields = ('created_at', 'updated_at',)