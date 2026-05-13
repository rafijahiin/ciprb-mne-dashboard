from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('baseline.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('mpdsr/', include('mpdsr.urls')),
    path('reports/', include('reports.urls')),
    # Add other URLs here later
]
