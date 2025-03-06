from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', include('my_demo_app.urls')),
]