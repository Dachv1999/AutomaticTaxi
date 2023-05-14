from django.db import models
from ManageEnterprise.models import Enterprise
from django.db.models.deletion import CASCADE

class Wallet(models.Model):
    code = models.CharField(max_length=50)
    money = models.CharField(max_length=30)

    def __str__(self):
        return self.code

class Person(models.Model):
    ci            = models.PositiveIntegerField(primary_key=True)
    name          = models.CharField(max_length=50)
    lastname      = models.CharField(max_length=50)
    date_birth    = models.DateField()
    city          = models.CharField(max_length=15)
    email         = models.EmailField(max_length=80, unique=True)
    password      = models.CharField(max_length=50)
    home          = models.CharField(max_length=50)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True


class Customer (Person):
    location  = models.CharField(max_length=80)
    is_Admin  = models.BooleanField(default=False)
    id_wallet = models.ForeignKey(Wallet,on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

class Owner (Person):
    token         = models.CharField(max_length=50)
    id_enterprise = models.ForeignKey(Enterprise,on_delete=CASCADE)

    def __str__(self):
        return self.nombre
    
