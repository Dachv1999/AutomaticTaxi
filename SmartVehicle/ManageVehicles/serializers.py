from .models import Vehicle, Transaction
from rest_framework import serializers

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehicle
        fields = ['plate','vehicle_state','batery','brake_system','suspension','tire_1','tire_2','tire_3','tire_4','model','year','cleaning','mileage','is_free','tax','latitud','longitud','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Transaction
        fields = ['id','plate_vehicle','customer','departure_place_lat','departure_place_long','arrival_place_lat','arrival_place_long','departure_time','arrival_time','rating','distance','price','comment','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)
