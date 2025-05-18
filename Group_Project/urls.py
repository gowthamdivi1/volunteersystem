from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin interface
    path('admin/', admin.site.urls),

    # Include application URLs from the 'catalog' app
    path('', include('catalog.urls')),
]
