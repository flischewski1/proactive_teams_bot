from django.urls import path 

from . import views



urlpatterns = [
    path("tutor/uploads", views.uploads, name="uploads"),
    path("tutor/activities", views.actvities, name="actvities"),
    path("tutor/reminder", views.reminder, name="reminder")
    
]