from django.urls import path
from .views import KoboIngestView

urlpatterns = [
    path('ingest/', KoboIngestView.as_view(), name='kobo-ingest'),
]
