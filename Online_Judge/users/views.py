from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect(reverse("login"))
    return render(request,"users/user.html")

def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"users/login.html")
    return render(request,"users/login.html") 

def logout_view(request):
    logout(request)
    return render(request,"users/login.html")

def home_page(request):
    return render(request, "users/home_page.html", {"page_name":"home_page"})

def practice(request):
    return render(request, "users/practice.html" , {"page_name":"practice_problems"})

def problem_statement(request):
    return render(request, "users/problem_statement.html", {"page_name":"problem_statemet"})

def submit(request):
    return render(request, "users/submit.html", {"page_name":"submit problem"})

def contest_page(request):
    return render(request, "users/contest_page.html", {"page_name":"lab #1"})

def developers(request):
    return render(request, "users/developers.html", {"page_name":"Developers"})

def mentors(request):
    return render(request, "users/mentors.html", {"page_name":"Mentors"})