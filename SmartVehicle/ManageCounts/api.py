from .models import Person
from rest_framework import viewsets, permissions
from .serializers import PersonSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('ci')
    serializer_class   = PersonSerializer
    permission_classes = [permissions.AllowAny]

""" class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('ci')
    serializer_class   = CustomerSerializer
    permission_classes = [permissions.AllowAny]

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by('ci')
    serializer_class   = OwnerSerializer
    permission_classes = [permissions.AllowAny] """