from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_view, name='root'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('demo/', views.demo_view, name='demo'),
    path('oauth_success/', views.oauth_success_view, name='oauth_success'),
    path('logged_in/', views.logged_in_view, name='logged_in'),
    path('logout/', views.logout_view, name='logout'),
]