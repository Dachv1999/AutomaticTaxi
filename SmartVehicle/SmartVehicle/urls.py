from django.contrib import admin
from django.urls import path, include

from ManageCounts.router import router_person
from ManageEnterprise.router import router_enterprise, router_invoice
from ManageVehicles.router import router_vehicle, router_transaction
from ManageCounts.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router_person.urls)),
    path('api/', include(router_enterprise.urls)),
    path('api/', include(router_invoice.urls)),
    path('api/', include(router_vehicle.urls)),
    path('api/', include(router_transaction.urls)),
    path('login/', login)
]
