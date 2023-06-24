from django.contrib import admin
from django.urls import path, include, register_converter
from . import converters
from ManageCounts.router import router_person
from ManageEnterprise.router import router_enterprise, router_invoice
from ManageEnterprise.views import create_pdf
from ManageVehicles.router import router_vehicle, router_transaction
from ManageCounts.views import login, logout, register
from ManageEnterprise.views import getPayInvoice, create_report_invoice, getNotPayInvoice
from ManageVehicles.views import getPriceTravel, endTravelplate, repairFails, startTravel, getAllTransaction, update_locations_randomly, search_Invoices, search_Transactions

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
    path('register/', register),
    path('getPrice/<str:latitud_user>/<str:longitud_user>/<int:traveldis>/', getPriceTravel),
    path('startTravel/', startTravel),
    path('endTravel/', endTravelplate),
    path('repair/', repairFails),

    path('getAllTransaction/<int:ci_user>/', getAllTransaction),
    path('getPayInvoice/', getPayInvoice),
    path('getNotPayInvoice/', getNotPayInvoice),
    path('createpdf/<int:id_invoice>/', create_pdf),
    path('updatelocations/', update_locations_randomly),
    path('create_report_invoice/<str:start_date>/<str:end_date>/', create_report_invoice),
    path('searchTransacciones/', search_Transactions),
    path('searchInvoice/', search_Invoices),
    
]
