from apscheduler.schedulers.background import BackgroundScheduler
import sys
import requests
import data_extraction.base_data_extraction as extraction
import datetime
from main.models import Team, Channel
from data_extraction.base_data_extraction import check_upload
from main.models import Messages, User, Team, Channel, FeedbackUpload, Upload, Reminder
import datetime
import modules.messageHandler as messageHandler
from dateutil import parser
from main.views import import_teams,import_channels,import_user,import_member
import json

# import relevant IDs
config = json.load(open("import_credentials.json", "r"))

vcl_team_id = config["vcl_team_id"]
channel_id_vcl = config["channel_id_vcl"]
e_tutoren_id = config["e_tutoren_id"]
channel_id_etutors = config["channel_id_etutors"]

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def get_subscription():
    print("subscirption startet")
    relevant_teams = Team.objects.filter(relevant=True)
    for team in relevant_teams: 
       relevant_channels = Channel.objects.filter(teamid = team.id)
       for channel in relevant_channels:
         
            httpanswer = subscribe(team.teamid, channel.channelid)
            if httpanswer.status_code == 200: 
                print("subscirption für" + team.teamid +" mit " + channel.channelid + " erfolgreich" + httpanswer)
            else:
                print(httpanswer.text)
                print("Subscription für Team: " + team.teamid +"ist bereits vollzogen oder ausgefallen")
                
# subscribe to channel
def subscribe(teamid,channelid):
    print("Subscription Service gestartet")
    ngrok_url = "https://06ca-212-204-40-18.eu.ngrok.io/api/messages"
    url= "https://graph.microsoft.com/v1.0/subscriptions"
    resource = f"teams/{teamid}/channels/{channelid}/messages"

    bearer_token = extraction.get_bearer_token()
    time = datetime.datetime.now() - datetime.timedelta(hours=1)
    time = time.isoformat()
    payload= {
        "changeType":"created",
        "notificationUrl":ngrok_url,
        "resource": resource,
        "expirationDateTime": str(time + "Z") ,
        "clientState": "secretClientValue"
    }
    headers = {
            'Authorization': 'Bearer ' + bearer_token,
            'Content-Type': 'application/json'
    }
    r = requests.post(url,headers=headers, json = payload)
    return r

# Use Case 3: Check upload folder general
def check_upload_general(): 
    file_list_raw = check_upload()
    file_list_names = []
    for file in file_list_raw: 
        
        try:
            # try to add new files
            uploaddate = parser.parse(file["createdDateTime"] )
            uploaddate = uploaddate + datetime.timedelta(hours=2) 
            u = Upload(fileid = file["id"], teamid = Team.objects.get(teamid=vcl_team_id), uploaddate=uploaddate, filename=file["name"])
            u.save()
            file_list_names.append(file["name"])
        except: 
            # except, if file already exists (file-id already saved)
            file_list_names.append(file["name"])
    feedback_needed = False 

    for file in file_list_names: 
        if "pdf" in file: 
            pass
        else:
            feedback_needed = True

    
    if feedback_needed:
        try: 
            #check team, if feedback has been already given. Exclude this exception to send feedback after each wrong upload
            FeedbackUpload.objects.get(teamid=Team.objects.get(teamid=vcl_team_id))
        except:
            message_feedback = """Hi all, I noticed that you uploaded some files into the Gen-eral-folder. Great job! :) I checked them and one or some of them are not pdf files. Please convert your file into pdf-format and upload them again,  so we won't loose points :). <br> 
                <br> Kind Regards <br> Hermine"""    #send message 
            messageHandler.send_channel_message(
        "Wrong File format", message_feedback, vcl_team_id, channel_id_vcl)
            f = FeedbackUpload(teamid=Team.objects.get(teamid=vcl_team_id), feedbackGivenPdf=True)
            f.save()
            print("Feedback sended")

# Use Case 2: Check saved Reminder dates and excecute them, if possible
def send_reminder():
    reminder_list = Reminder.objects.all()
    for reminder in reminder_list:
        n = datetime.datetime.now() 
        r = reminder.triggerdate

        # check date of reminder
        diff = r.replace(tzinfo=None) - n.replace(tzinfo=None) 
        if datetime.timedelta(minutes=1) > diff :
            answer = messageHandler.send_channel_message(reminder.subject,reminder.body, vcl_team_id, channel_id_vcl)   
            print(answer)
            reminder.delete() 

"""
Synchronisierungsservice
"""
def synchonize_base_data(): 
    import_teams()
    import_user()
    import_channels()
    import_member()
    pass

# Scheduler function to configure scheduler jobs
def start():
    
    scheduler = BackgroundScheduler()

    scheduler.add_job(get_subscription, 'interval', hours = 1.000001, name='get_subs', jobstore='default')
    scheduler.add_job(check_upload_general, 'interval', minutes = 1, name='check_upload', jobstore='default')
    scheduler.add_job(send_reminder, 'interval', minutes = 0.5, name='send_reminder', jobstore='default')
    scheduler.add_job(synchonize_base_data, 'interval', minutes = 5, name='synchonize_base_data', jobstore='default')

    scheduler.start()
    print("Scheduler started...", file=sys.stdout)