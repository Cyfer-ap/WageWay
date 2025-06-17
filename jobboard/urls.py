from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('my-posts/', views.my_posted_jobs, name='my_posted_jobs'),
    path('applied/', views.my_applications, name='my_applications'),
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('application/<int:application_id>/accept/', views.accept_application, name='accept_application'),
    path('application/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('application/<int:application_id>/confirm-completion/', views.confirm_job_completion, name='confirm_job_completion'),

]
