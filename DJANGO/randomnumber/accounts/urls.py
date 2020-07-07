from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("resister",views.resister,name="resister"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("call_api",views.call_api,name="call_api"),
    path("see_remaining_limits",views.see_remaining_limits,name="see_remaining_limits")]