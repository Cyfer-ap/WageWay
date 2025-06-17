from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('services/', include('services.urls')),
    path('bookings/', include('bookings.urls')),
    path('messages/', include('notifications.urls')),
    path('notifications/', include('notifications.urls')),
    path('emails/', include('emails.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)