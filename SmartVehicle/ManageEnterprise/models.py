from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.deletion import CASCADE

class Enterprise(models.Model):
    enterprise_name = models.CharField(max_length=25, unique=True)
    email           = models.EmailField(max_length=80, unique=True)
    budget          = models.DecimalField(max_digits=5, decimal_places=2)
    location        = models.CharField(max_length=80)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Invoice(models.Model):
    nit          = models.PositiveIntegerField(primary_key=True ,validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    id_empresa   = models.ForeignKey(Enterprise,on_delete=CASCADE)
    service_desc = models.CharField(max_length=100)
    price        = models.DecimalField(max_digits=5, decimal_places=2)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nit