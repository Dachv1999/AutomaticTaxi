from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ManageCounts.models import Customer
from django.db.models.deletion import CASCADE 

class Vehicle(models.Model):
    State         = (('B', "Bueno"), ('R', "Regular"), ('M', "Malo"))
    plate         = models.CharField(primary_key=True, max_length=50)
    vehicle_state = models.CharField(default='B', choices=State, max_length=1)
    fuel          = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    oil           = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_1        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_2        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_3        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    tire_4        = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    model         = models.CharField(max_length=20)
    year          = models.PositiveIntegerField(default=2023,  validators=[MinValueValidator(1990), MaxValueValidator(2023)])
    cleaning      = models.PositiveIntegerField(default=100,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    mileage       = models.PositiveIntegerField()   
    tax           = models.DecimalField(max_digits=5, decimal_places=2)
    location      = models.CharField(max_length=80)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plate


class Transaction(models.Model):
    plate_vehicle   = models.ForeignKey(Vehicle,on_delete=CASCADE)
    ci_customer     = models.ForeignKey(Customer,on_delete=CASCADE)
    departure_place = models.CharField(max_length=80)
    arrival_place   = models.CharField(max_length=80)
    departure_time  = models.DateTimeField()
    arrival_time    = models.DateTimeField()
    rating          = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    distance        = models.PositiveIntegerField() 
    price           = models.DecimalField(max_digits=5 ,decimal_places=2)
    comment         = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)






