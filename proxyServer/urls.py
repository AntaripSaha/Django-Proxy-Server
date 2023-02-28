from django.urls import path
from .views import active_ips, ping_ips, available_ips, set_proxy

urlpatterns = [
    path('active_ips/', active_ips, name='active_ips'),
    path('ping_ips/', ping_ips, name='ping_ips'),
    path('available_ips/', available_ips, name='available_ips'),
    path('select_ip/<str:ip_port>/', set_proxy, name='select_ip')
]
