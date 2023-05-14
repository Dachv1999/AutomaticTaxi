from .models import Wallet, Customer, Owner
from rest_framework import viewsets, permissions
from .serializers import WalletSerializer, CustomerSerializer, OwnerSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class   = WalletSerializer
    permission_classes = [permissions.AllowAny]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('ci')
    serializer_class   = CustomerSerializer
    permission_classes = [permissions.AllowAny]

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by('ci')
    serializer_class   = OwnerSerializer
    permission_classes = [permissions.AllowAny]