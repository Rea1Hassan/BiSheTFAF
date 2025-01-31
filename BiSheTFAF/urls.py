
from TFAFapp import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # 根路径指向index视图
    path('get_location/', views.get_location, name='get_location'),  # 地理编码API接口
    path('query-traffic-status/', views.query_traffic_status, name='query_traffic_status'),
]