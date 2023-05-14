from rest_framework.routers import DefaultRouter
from .api import VehicleViewSet, TransactionViewSet

router_vehicle   = DefaultRouter()
router_transaction = DefaultRouter()

router_vehicle.register(prefix='vehicle', basename='vehicle', viewset=VehicleViewSet)
router_transaction.register(prefix='transaction', basename='transaction', viewset=TransactionViewSet)
