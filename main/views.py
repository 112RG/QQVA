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
    return render(response, "main/command.html", {})

#help page
def help(response):
    return render(response, "main/help.html", {})

#admin page
def admin(response):
    return render(response, "main/admin.html", {})

#login page
def login(response):
    return render(response, "main/login.html", {})

#registration page
def rego(response):
    return render(response, "main/rego.html", {})