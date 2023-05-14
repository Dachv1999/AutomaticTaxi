from rest_framework.routers import DefaultRouter
from .api import EnterpriseViewSet, InvoiceViewSet

####################################################################
##                  Arma las rutas para el CRUD                   ## 
####################################################################

router_enterprise   = DefaultRouter()
router_invoice      = DefaultRouter()

router_enterprise.register(prefix='enterprise', basename='enterprise', viewset=EnterpriseViewSet)
router_invoice.register(prefix='invoice', basename='invoice', viewset=InvoiceViewSet)
