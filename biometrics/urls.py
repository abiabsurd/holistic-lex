from django.urls import path

from biometrics.views import client_metrics

urlpatterns = [
    path('client-metrics/<int:pk>/', client_metrics, name='client_metrics'),
]
