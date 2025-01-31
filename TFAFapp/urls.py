# TFAFapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('traffic-data/', views.traffic_data, name='traffic_data'),
    # 其他路径...
]