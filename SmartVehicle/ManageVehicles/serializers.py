from .models import Vehicle, Transaction
from rest_framework import serializers

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehicle
        fields = ['plate','vehicle_state','fuel','price','oil','tire_1','tire_2','tire_3','tire_4','model','year','cleaning','mileage','tax','location','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Transaction
        fields = ['id','plate_vehicle','ci_customer','departure_place','arrival_place','departure_time','arrival_time','rating','distance','price','comment','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)
