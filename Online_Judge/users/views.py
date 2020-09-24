from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect(reverse("login"))
    x = Submission.objects.all().first()
    print(x.lang)
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

    