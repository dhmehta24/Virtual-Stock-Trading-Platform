from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register_user, name = "register_user"),
    path('update_profile',views.update_profile, name = "update_profile"),
    path('login',views.login_user, name = "login_user"),
    path('logout', views.logout_user, name = "logout_user"),
]