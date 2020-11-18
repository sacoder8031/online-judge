from users.views import home_page
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("home_page/<int:blog_id>", views.home_page_blog, name="blog"),
    path("home_page",views.home_page , name="home_page"),
    path("lab_works",views.lab_works , name="lab_works"),
    path("tutorial",views.tutorial , name="tutorial"),
    path("profile",views.profile , name="profile"),
    path("practice",views.practice , name="practice"),
    path("problem_statement",views.problem_statement , name="problem_statement"),
    path("submit",views.submit , name="submit"),
    path("contest_page",views.contest_page , name="contest_page"),
    path("developers",views.developers , name="developers"),
    path("mentors",views.mentors , name="mentors"),
    #path("register",views.register,name="register")
]
