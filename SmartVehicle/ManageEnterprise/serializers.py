from .models import Enterprise
from ManageVehicles.models import  Invoice, Invoice_extended
from rest_framework import serializers

class EnterpriseSerializer(serializers.ModelSerializer):#clase para lo que el JSON devolvera
    class Meta:
        model  = Enterprise
        fields = ['id','enterprise_name','email','cuenta','private_key','budget','latitud','longitud','taxes','created_at','updated_at']
        read_only_fields = ('created_at', 'updated_at',) #atributos que no podra modificar

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Invoice
        fields = ['id','nit','id_empresa','service_desc','price','plate','is_pay','created_at','updated_at']
        read_only_fields = ('created_at', 'updated_at',)

class AllInvoiceSerializer(serializers.ModelSerializer):
    invoice_id = InvoiceSerializer(many=True)
    class Meta:
        model  = Invoice_extended
        fields = ['invoice_id']
