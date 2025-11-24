from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),  # core app home page
    path('users/', include('users.urls')), 
    path('dashboard/', include('dashboard.urls')),
    path('tasks/', include('tasks.urls')),

 


]
