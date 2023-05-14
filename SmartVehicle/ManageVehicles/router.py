from rest_framework.routers import DefaultRouter
from .api import VehicleViewSet, TransactionViewSet

####################################################################
##                  Arma las rutas para el CRUD                   ## 
####################################################################

router_vehicle   = DefaultRouter()
router_transaction = DefaultRouter()

router_vehicle.register(prefix='vehicle', basename='vehicle', viewset=VehicleViewSet)
router_transaction.register(prefix='transaction', basename='transaction', viewset=TransactionViewSet)
