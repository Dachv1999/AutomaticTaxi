from .models import Vehicle, Transaction
from rest_framework import viewsets, permissions
from .serializers import VehicleSerializer, TransactionSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('plate')
    serializer_class   = VehicleSerializer
    permission_classes = [permissions.AllowAny]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class   = Transaction
    permission_classes = [permissions.AllowAny]