from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.create_booking, name='create_booking'),
    path('my/', views.customer_bookings, name='my_bookings'),
    path('provider/', views.provider_bookings, name='provider_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('confirm/provider/<int:booking_id>/', views.mark_provider_completed, name='provider_confirm_booking'),
    path('confirm/customer/<int:booking_id>/', views.mark_customer_completed, name='customer_confirm_booking'),
]
