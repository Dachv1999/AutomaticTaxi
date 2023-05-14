from .models import Enterprise, Invoice
from rest_framework import serializers

class EnterpriseSerializer(serializers.ModelSerializer):#clase para lo que el JSON devolvera
    class Meta:
        model  = Enterprise
        fields = ['id','enterprise_name','email','budget','location','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',) #atributos que no podra modificar

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Invoice
        fields = ['nit','id_empresa','service_desc','price','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)