from django.urls import path
from . import views
from .views import notification_list

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('', notification_list, name='notifications'),
]
