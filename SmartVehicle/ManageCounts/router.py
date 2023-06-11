from rest_framework.routers import DefaultRouter
from .api import PersonViewSet

####################################################################
##                  Arma las rutas para el CRUD                   ## 
####################################################################

router_person = DefaultRouter()

router_person.register(prefix='person', basename='router', viewset=PersonViewSet)

""" router_customer = DefaultRouter()
router_owner    = DefaultRouter()

router_customer.register(prefix='router', basename='router', viewset=CustomerViewSet)
router_owner.register(prefix='owner', basename='owner', viewset=OwnerViewSet) """
