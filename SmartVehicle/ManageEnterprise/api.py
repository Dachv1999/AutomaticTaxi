from .models import Enterprise
from ManageVehicles.models import Invoice
from rest_framework import viewsets, permissions
from .serializers import EnterpriseSerializer, InvoiceSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################

class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class   = EnterpriseSerializer
    permission_classes = [permissions.AllowAny]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('id')
    serializer_class   = InvoiceSerializer
    permission_classes = [permissions.AllowAny]