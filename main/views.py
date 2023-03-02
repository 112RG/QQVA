from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# pg - creating 6 views one for each page, related to urls.py

#home page
def home(response):
    return HttpResponse("home Page!")

#home page
def command(response):
    return HttpResponse("Command Log!")

#home page
def help(response):
    return HttpResponse("Help Page!")

#home page
def admin(response):
    return HttpResponse("Admin Page!")

#home page
def login(response):
    return HttpResponse("Login Page!")

#home page
def rego(response):
    return HttpResponse("Registration Page!")