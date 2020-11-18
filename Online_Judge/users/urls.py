from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("home_page",views.home_page , name="home_page"),
    path("lab_works",views.lab_works , name="lab_works"),
    path("tutorial",views.tutorial , name="tutorial"),
    path("profile",views.profile , name="profile"),
    #path("register",views.register,name="register")
]
