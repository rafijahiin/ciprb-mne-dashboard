from django.contrib import admin
from django.urls import path, include
from dashboard.views import landing_page
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', landing_page, name='landing'),
    path('api/kobo/', include('baseline.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('mpdsr/', include('mpdsr.urls')),
    path('reports/', include('reports.urls')),
    path('activities/', include('activities.urls')),
]
