from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.deletion import CASCADE

class Enterprise(models.Model):
    enterprise_name = models.CharField(max_length=25, unique=True)
    email           = models.EmailField(max_length=80, unique=True)
    cuenta          = models.CharField(max_length=255, unique=True, null=True)
    private_key     = models.CharField(max_length=255, unique=True, null=True)
    budget          = models.DecimalField(max_digits=8, decimal_places=2)
    longitud        = models.FloatField(blank=True, null=True)
    latitud         = models.FloatField(blank=True, null=True)
    taxes           = models.DecimalField(max_digits=8, decimal_places=2, null=True) 
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.enterprise_name

class Invoice(models.Model):
    nit          = models.CharField(max_length=255, unique=True, null=True)
    id_empresa   = models.ForeignKey(Enterprise,on_delete=CASCADE)
    service_desc = models.TextField(max_length=100)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    is_pay       = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nit
    
class Invoice_extended(models.Model):
    
    invoice_id = models.ForeignKey(Invoice, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.invoice_id)