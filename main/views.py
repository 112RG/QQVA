from django.shortcuts import render
from django.http import HttpResponse
from .models import Command
# Create your views here.
# pg - creating 6 views one for each page, related to urls.py

#home page
def home(response):
    # old code - return HttpResponse("home Page!")
    context = {
        'image_path': 'images/example.jpg'
    }
    return render(response, "main/home.html", {})

#command page
def command(response):
    rows = Command.objects.all().order_by('-command_time')
    return render(response, "main/command.html", {'rows': rows})
#visual page
def visual(response):
    return render(response, "main/visual.html", {})
#help page
def help(response):
    return render(response, "main/help.html", {})

#admin page
def admin(response):
    return render(response, "main/admin.html", {})