from django.urls import path
from . import views

urlpatterns = [
    path('provider/', views.service_list_provider, name='provider_services'),
    path('provider/add/', views.service_create, name='service_create'),
    path('provider/<int:pk>/edit/', views.service_update, name='service_update'),
    path('provider/<int:pk>/delete/', views.service_delete, name='service_delete'),

    path('browse/', views.service_list_customer, name='service_browse'),
    path('browse/<int:pk>/', views.service_detail, name='service_detail'),
]

