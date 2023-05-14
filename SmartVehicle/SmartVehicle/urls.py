from django.contrib import admin
from django.urls import path, include

from ManageCounts.router import router_wallet, router_customer, router_owner
from ManageEnterprise.router import router_enterprise, router_invoice
from ManageVehicles.router import router_vehicle, router_transaction


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router_customer.urls)),
    path('api/', include(router_owner.urls)),
    path('api/', include(router_wallet.urls)),
    path('api/', include(router_enterprise.urls)),
    path('api/', include(router_invoice.urls)),
    path('api/', include(router_vehicle.urls)),
    path('api/', include(router_transaction.urls))
]
