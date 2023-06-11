from .models import Vehicle, Transaction, Transaction_extended
from rest_framework import serializers

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehicle
        fields = ['plate','vehicle_state','batery','brake_system','suspension','tire_1','tire_2','tire_3','tire_4','model','year','cleaning','mileage','is_free','tax','latitud','longitud','created_at','updated_at']
        read_only_fields = ('created_at', 'updated_at',)



class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Transaction
        fields = ['id','travel_type','departure_place_lat','departure_place_long','arrival_place_lat','arrival_place_long','departure_time','arrival_time','rating','distance','price','comment','created_at','updated_at']
        read_only_fields = ('created_at', 'updated_at',)

class AllTransactionSerializer(serializers.ModelSerializer):
    transaction_id = TransactionSerializer(many=True)
    class Meta:
        model  = Transaction_extended
        fields = ['transaction_id']

