from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# pg - creating 6 views one for each page, related to urls.py

#home page
def home(response):
    # old code - return HttpResponse("home Page!")
    return render(response, "main/home.html", {})

#command page
def command(response):
    return HttpResponse("Command Log!")

#help page
def help(response):
    return HttpResponse("Help Page!")

#admin page
def admin(response):
    return HttpResponse("Admin Page!")

#login page
def login(response):
    return HttpResponse("Login Page!")

#registration page
def rego(response):
    return HttpResponse("Registration Page!")