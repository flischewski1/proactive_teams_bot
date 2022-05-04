from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
# view is like a webpage

def index(response): 
    return HttpResponse("Hello World!")

def controlModel(response): 
    return HttpResponse("<a> MOINN </a>")