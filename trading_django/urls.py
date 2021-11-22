from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('trading.urls')),
    path('internal/', include('internal_transfer.urls')),
    path('pay24/', include('Pay24.urls'))
]

urlpatterns += doc_urls
