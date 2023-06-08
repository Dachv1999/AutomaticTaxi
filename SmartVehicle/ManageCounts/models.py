from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

####################################################################
##          Funciones object para crear user y suoeruser          ## 
####################################################################

class UsuarioManager(BaseUserManager): 
    
    def create_user(self, ci, email, password):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico!')

        user = self.model(
            ci       = ci,
            email    = self.normalize_email(email),
            password = password,
        )
        
        #user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ci, email, password):

        user = self.create_user(
            ci       = ci,
            email    = email,
            password = password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


############################################################################
##      Overide de la clase User para definir mis propios atributos       ## 
############################################################################

class Person(AbstractBaseUser):
    ci            = models.AutoField(primary_key=True)
    name          = models.CharField(max_length=50, blank=True, null=True)
    lastname      = models.CharField(max_length=50, blank=True, null=True)
    city          = models.CharField(max_length=15, blank=True, null=True)
    email         = models.EmailField(max_length=80, unique=True)
    home          = models.CharField(max_length=50, blank=True, null=True)
    is_active     = models.BooleanField(default=True)
    is_superuser  = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    longitud      = models.FloatField(blank=True, null=True)
    latitud       = models.FloatField(blank=True, null=True)

    date_joined   = models.DateTimeField(default=timezone.now)
    last_login    = models.DateTimeField(blank=True, null=True)

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    objects       = UsuarioManager() 

    USERNAME_FIELD  = 'email'
    EMAIL_FIELD     = 'email'
    REQUIRED_FIELDS = ['ci']

    def __str__(self):
        return str(self.name)
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    """ @property
    def is_staff(self):
        return self.is_superuser """


""" class Customer (models.Model):
    user     = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    longitud = models.CharField(max_length=80, blank=True, null=True)
    latitud  = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return self.name

class Owner (models.Model):
    user          = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    token         = models.CharField(max_length=255, unique=True, blank=True, null=True)
    id_enterprise = models.ForeignKey(Enterprise,on_delete=CASCADE)

    def __str__(self):
        return self.name """
    
