
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finlife.urls')),
    path('exchange/', include('exchange.urls')),
]
