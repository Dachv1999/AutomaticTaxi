from django.contrib import admin
from django.urls import path, include, register_converter
from . import converters
from ManageCounts.router import router_person
from ManageEnterprise.router import router_enterprise, router_invoice
from ManageEnterprise.views import create_pdf
from ManageVehicles.router import router_vehicle, router_transaction
from ManageCounts.views import login, logout
from ManageVehicles.views import getPriceTravel, endTravelplate, repairFails, startTravel, update_locations_randomly

register_converter(converters.FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router_person.urls)),
    path('api/', include(router_enterprise.urls)),
    path('api/', include(router_invoice.urls)),
    path('api/', include(router_vehicle.urls)),
    path('api/', include(router_transaction.urls)),
    path('login/', login),
    path('logout/', logout),
    path('getPrice/<str:latitud_user>/<str:longitud_user>/<int:traveldis>/', getPriceTravel),
    path('startTravel/', startTravel),
    path('endTravel/', endTravelplate),
    path('repair/', repairFails),
    path('createpdf/<int:id_invoice>/', create_pdf),
    path('updatelocations/', update_locations_randomly)
    
]
