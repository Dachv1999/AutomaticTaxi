from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from ManageCounts.models import Person
from ManageEnterprise.models import Enterprise
from django.db.models.deletion import CASCADE 

class Vehicle(models.Model):
    State         = (('B', "Bueno"), ('R', "Regular"), ('M', "Malo"))
    plate         = models.CharField(primary_key=True, max_length=50)
    vehicle_state = models.CharField(default='B', choices=State, max_length=1)
    batery        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    brake_system  = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    suspension    = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_1        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_2        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_3        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_4        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    model         = models.CharField(max_length=20)
    year          = models.PositiveIntegerField(default=2023,  validators=[MinValueValidator(1990), MaxValueValidator(2023)])
    cleaning      = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    mileage       = models.PositiveIntegerField()   
    is_free       = models.BooleanField(default= True)
    tax           = models.DecimalField(max_digits=8, decimal_places=2)
    longitud      = models.FloatField(blank=True, null=True)
    latitud       = models.FloatField(blank=True, null=True)
    id_enterprise = models.ForeignKey(Enterprise,on_delete=CASCADE, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plate


class Transaction(models.Model):
    Travel         = (('V', "Viaje"), ('D', "Delivery"), ('O', "Otros"))
    plate_vehicle   = models.ForeignKey(Vehicle,on_delete=CASCADE)
    customer        = models.ForeignKey(Person,on_delete=models.CASCADE, null=True)
    travel_type     = models.CharField(default='V', choices=Travel, max_length=1)
    departure_place_lat  = models.FloatField(blank=True, null=True)
    departure_place_long = models.FloatField(blank=True, null=True)
    arrival_place_lat    = models.FloatField(blank=True, null=True)
    arrival_place_long   = models.FloatField(blank=True, null=True)
    departure_time  = models.DateTimeField(blank=True, null=True)
    arrival_time    = models.DateTimeField(blank=True, null=True)
    rating          = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    distance        = models.PositiveIntegerField(default=0) 
    price           = models.DecimalField(max_digits=8 ,decimal_places=2, blank=True, null=True)
    comment         = models.CharField(max_length=100, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.price)
    
class Transaction_extended(models.Model):
    
    transaction_id = models.ForeignKey(Transaction, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.transaction_id)




