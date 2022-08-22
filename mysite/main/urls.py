from django.urls import path 

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path('api/messages', views.notification_hub, name="notification_hub"),
    path('api/import_member', views.import_member, name="import_member"),
    path('api/import_teams', views.import_teams, name="import_teams"),
    path('api/import_user', views.import_user, name="import_user"),
    path('api/import_channels', views.import_channels, name="import_channels"),
    path('api/check_activity_user', views.check_activity_user, name="check_activity_user"),
    path('api/check_sign_ins', views.check_sign_ins, name="check_sign_ins"),
    path('api/reminder', views.reminder, name="reminder")
]