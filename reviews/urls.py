from django.urls import path
from . import views

urlpatterns = [
    path('job/<int:job_id>/review-worker/', views.review_worker, name='review_worker'),
    path('job/<int:job_id>/review-poster/', views.review_poster, name='review_poster'),
]
