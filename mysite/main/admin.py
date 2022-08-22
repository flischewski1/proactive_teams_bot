from django.contrib import admin
from main.models import Team, Channel, User, Messages, Upload, FeedbackUpload, Reminder

# Register your models here.
admin.site.register(Team) # admin
admin.site.register(Channel) 
admin.site.register(User) 
admin.site.register(Messages) 
admin.site.register(Upload) 
admin.site.register(FeedbackUpload) 
admin.site.register(Reminder) 