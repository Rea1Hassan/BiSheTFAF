
from TFAFapp import views
from django.contrib import admin
from django.urls import include, path,re_path
from TFAFapp.views import calculate_rect_bounds_and_query
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # 根路径指向index视图
    path('get_location/', views.get_location, name='get_location'),  # 地理编码API接口
    path('query-traffic-status/', views.query_traffic_status, name='query_traffic_status'),
    path('calculate_rect_bounds_and_query/', views.calculate_rect_bounds_and_query,
         name='calculate_rect_bounds_and_query'),  # 矩形交通态势

    # 支持以.html结尾的URL
    re_path(r'^rectangle_traffic_status\.html$', TemplateView.as_view(template_name="rectangle_traffic_status.html"),
            name='rectangle_traffic_status_html'),

    # 原有的支持/rectangle_traffic_status/的路径
    path('rectangle_traffic_status/', TemplateView.as_view(template_name="rectangle_traffic_status.html"),
         name='rectangle_traffic_status'),
]