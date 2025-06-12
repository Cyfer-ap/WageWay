from django.urls import path
from .views import home, dashboard, register_customer, register_provider, CustomLoginView, customer_dashboard, \
    provider_dashboard, customer_profile, provider_profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/customer/', register_customer, name='register_customer'),
    path('register/provider/', register_provider, name='register_provider'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/customer/', customer_dashboard, name='customer_dashboard'),
    path('dashboard/provider/', provider_dashboard, name='provider_dashboard'),
    path('profile/customer/', customer_profile, name='customer_profile'),
    path('profile/provider/', provider_profile, name='provider_profile'),

]
