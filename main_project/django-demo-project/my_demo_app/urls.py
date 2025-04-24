from django.urls import path
from . import views

urlpatterns = [
    path("", views.root_view, name="root"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("demo/", views.demo_view, name="demo"),
    path("oauth_success/", views.oauth_success_view, name="oauth_success"),
    path("logged_in/", views.logged_in_view, name="logged_in"),
    path("logout/", views.logout_view, name="logout"),
    path("documents/<int:doc_id>/", views.latex_editor_view, name="latex_editor"),
    path("documents/", views.logged_in_view, name="document_list"),
    path('documents/<int:doc_id>/delete/', views.delete_document,name='document_delete'),
]