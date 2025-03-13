from django.urls import path
from .views import demo_view, root_view, register_view, login_view, oauth_success_view, forgot_password_view, logged_in_view, logout_view

urlpatterns = [
    path('demo/', demo_view, name='demo'),
    path('', root_view, name='root'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('oauth-success/', oauth_success_view, name='oauth_success'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('logged-in/', logged_in_view, name='logged_in'),
    path('logout/', logout_view, name='logout'),
]