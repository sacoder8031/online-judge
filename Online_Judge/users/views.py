from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request,"users/home_page.html")

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
    return render(request, "users/home_page.html",{
        "page_name":"home_page"
    })

def lab_works(request):
    return render(request, "users/lab_works.html",{
        "page_name":"lab_works"
    })

def tutorial(request):
    return render(request, "users/tutorial.html",{
        "page_name":"tutorial"
    })

def profile(request):
    return render(request, "users/profile.html",{
        "page_name":"profile"
    })
