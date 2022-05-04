from django.urls import path 
# importiere alles von views im aktuellen working directory 
from . import views 

urlpatterns = [
    # wichtig! der zweite parameter ist entscheidend
    path("", views.index, name="index"),
    path("v1/", views.controlModel, name="controlModel")
]