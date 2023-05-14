from rest_framework.routers import DefaultRouter
from .api import WalletViewSet, CustomerViewSet, OwnerViewSet

router_wallet   = DefaultRouter()
router_customer = DefaultRouter()
router_owner    = DefaultRouter()

router_wallet.register(prefix='wallet', basename='wallet', viewset=WalletViewSet)
router_customer.register(prefix='router', basename='router', viewset=CustomerViewSet)
router_owner.register(prefix='owner', basename='owner', viewset=OwnerViewSet)
