from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.create_booking, name='create_booking'),
    path('my/', views.customer_bookings, name='my_bookings'),
    path('provider/', views.provider_bookings, name='provider_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
