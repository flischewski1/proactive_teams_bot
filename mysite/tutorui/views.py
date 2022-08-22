from django.shortcuts import render
from main.models import Team, Channel, Upload, Reminder



# Create your views here.

def uploads(response):
    u = Upload.objects.all()
    return render(response, "tutorui/uploads.html", {"u":u})

def actvities(response):
    return render(response, "tutorui/actvities.html", {})

def reminder(response):
    reminder = Reminder.objects.all()
    return render(response, "tutorui/reminder.html", {"reminder": reminder})
    