import re
from django.http import HttpResponse
import datetime
from data_extraction.base_data_extraction import import_team_data, import_user_data, import_member_data, import_group_data, import_sign_ins, check_upload
from .models import Team, Channel, User
import data_extraction.base_data_extraction
from urllib.parse import parse_qs
from urllib.parse import urlparse
from django.views.decorators.csrf import csrf_exempt
import json
from main.models import Messages, User, Team, Channel, FeedbackUpload, Upload, Reminder
import datetime
import modules.messageHandler as messageHandler


config = json.load(open("import_credentials.json", "r"))


"""
Message Monitoring
"""

# Inserts incoming Message into database


def save_message(content, contenttype, channelid, teamid, userid):
    m = Messages(userid=User.objects.get(userid=userid), channelid=Channel.objects.get(
        channelid=channelid), body=content, contenttype=contenttype, teamid=Team.objects.get(teamid=teamid))
    m.save(Messages.objects.all())
    pass


def store_check_message(message_request):
    # channel id, user id, message text
    content = message_request['body']['content']
    contenttype = message_request['body']['contentType']
    channelid = message_request['channelIdentity']['channelId']
    teamid = message_request['channelIdentity']['teamId']
    userid = message_request['from']['user']['id']

    # check if user has sendet a message already
    check_activity_on_message(content, contenttype, channelid, teamid, userid)

    search_for_question(content, contenttype, channelid, teamid, userid)


def index(response):
    return HttpResponse("")


# Hub for each message of relevant teams


@csrf_exempt
def notification_hub(request):

    # returns validation token of subscription, if needed
    try:
        parsed_url = urlparse(request.get_full_path())
        token = parse_qs(parsed_url.query)['validationToken'][0]
        return HttpResponse(token)

    # takes the incomming message meta data and requests the resource data of the startmessage (len = 3) or reply (len = 4)
    except:
        message_string = None
        message_string = json.loads(request.body)['value'][0]['resource']
        message_list = message_string.split("/")
        request_list = []
        for s in message_list:
            ids = s[s.find("(")+1:s.find(")")].replace("'", "")
            request_list.append(ids)
        # get content if message is a reply
        if len(message_list) == 4:
            channelid = request_list[1]
            messageid = request_list[3]
            message_request = data_extraction.base_data_extraction.get_reply(
                request_list[0], channelid, request_list[2], messageid)
            store_check_message(message_request)

        # get content if message is a new thread
        if len(message_list) == 3:
            channelid = request_list[1]
            messageid = request_list[2]
            message_request = data_extraction.base_data_extraction.get_message(
                request_list[0], channelid, messageid)
            store_check_message(message_request)

        # print(message_request)
        return HttpResponse("")


"""
Synchronisierungsservice
"""

# get all Teams


def import_teams():

    teams_list = import_group_data()
    for i in range(0, len(teams_list)):
        try:
            team = teams_list[i]
            t = Team(teamid=team["id"],
                     displayName=team["displayName"], relevant=True)
            t.save()
            print(team["displayName"] + " wurde hinzugefügt")
        except:
            pass


def import_channels():

    # get all Teams

    relevant_teams = Team.objects.all()
    for team in relevant_teams:
        try:
            all_channels = import_team_data(team.teamid)
            for channel in all_channels:
                s = Channel(
                    teamid=team, channelid=channel["id"], displayName=channel["displayName"])
                s.save()
        except:
            pass


def import_user():

    # get all Teams
    user_list = import_user_data()
    for user in user_list:
        try:
            u = User(userid=user["id"], displayName=user["displayName"])
            u.save()
        except:
            pass


def import_member():
    teams = Team.objects.all()
    for team in teams:
        # get Team object

        member_data = import_member_data(team.teamid)
        for member in member_data:
            u = User.objects.get(userid=member["id"])
            try:
                u.teamid.add(team)
            except:
                pass


"""
Service Views, Use Case 1a, 1b
"""


vcl_team_id = config["vcl_team_id"]
channel_id_vcl = config["channel_id_vcl"]
e_tutoren_id = config["e_tutoren_id"]
channel_id_etutors = config["channel_id_etutors"]

activity_message = """Dear all, I noticed that some students didn't wrote a single message in their teams: """


@csrf_exempt
def check_activity_user(response):
    u = list(User.objects.exclude(
        firstmessage__isnull=False).values_list('displayName', flat=True))
    userid_list = list(User.objects.exclude(
        firstmessage__isnull=False).values_list('userid', flat=True))

    message_tutors = f"""Hi all, I noticed that some students didn't wrote a single message in their teams: <br> {u} <br> 
                I will contact each one and provide them with support and a guide, how they can use Microsoft Teams! <br>
                <br> Kind Regards <br> Hermine """

    messageHandler.send_channel_message(
        "Inactive Users", message_tutors, e_tutoren_id, channel_id_etutors)
    message_users = """<div> <div itemprop='copy-paste-block'><span><span>Hi, how are you? I recognized, that you haven't posted any message in our Teams yet. If you don't know how to start a conversation, don't worry, you will learn it in a minute using this website <a href='https://internal.support.services.microsoft.com/en-us/office/send-a-message-to-a-channel-in-teams-5c8131ce-eaad-4798-bc73-e33f4652a9c4#:~:text=%20Send%20a%20message%20to%20a%20channel%20in,lower%20left%20on%20the%20Posts%20tab.%20More%20' rel='noreferrer noopener' target='_blank' title='https://internal.support.services.microsoft.com/en-us/office/send-a-message-to-a-channel-in-teams-5c8131ce-eaad-4798-bc73-e33f4652a9c4#:~:text=%20send%20a%20message%20to%20a%20channel%20in,lower%20left%20on%20the%20posts%20tab.%20more%20'>Send a message to a channel in Teams (microsoft.com)</a> ! <span class='animated-emoticon-20' title='Smile' type='smile'><img itemid='smile' itemscope='' itemtype='http://schema.skype.com/Emoji' src='https://statics.teams.cdn.office.net/evergreen-assets/personal-expressions/v2/assets/emoticons/smile/default/20_f.png?v=v79' alt='🙂' style='width:20px; height:20px'></span>​</span></span></div> </div>"""
    for userid in userid_list:
        messageHandler.send_user_message(message_users, userid)
        print(userid)
    return HttpResponse(200)


def check_activity_on_message(content, contenttype, channelid, teamid, userid):
    try:
        Messages.objects.get(userid=userid)
        save_message(content, contenttype, channelid, teamid, userid)
    except:
        save_message(content, contenttype, channelid, teamid, userid)
        u = User.objects.get(userid=userid)
        u.firstmessage = datetime.datetime.now()
        u.save()


@csrf_exempt
def check_sign_ins(response):
    sign_ins_list = import_sign_ins()
    sign_ins_user_id = set([])
    for user in sign_ins_list:
        sign_ins_user_id.add(user["userId"])
    all_user_id = set(User.objects.values_list('userid', flat=True))
    not_active = all_user_id.difference(sign_ins_user_id)
    not_active_objects = [User.objects.get(
        userid=user_id) for user_id in not_active]
    not_active_displayName = [user.displayName for user in not_active_objects]
    message_not_active = f"""Hi all, I noticed that these students didn't sign in into Microsoft Office 365: <br> {not_active_displayName} <br> <br> 
                            Please contact them, if they need support accessing Teams or if they want to continue the course. <br> 
                            <br> Kind Regards <br> Hermine"""
    messageHandler.send_channel_message(
        "No Sign In yet", message_not_active, e_tutoren_id, channel_id_etutors)
    return HttpResponse(200)


"""
Service views, Use Case 2
"""


@csrf_exempt
def reminder(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        r = Reminder(teamid=Team.objects.get(teamid=vcl_team_id),
                     triggerdate=body["triggerdate"], subject=body["subject"], body=body["body"])
        r.save()
        return HttpResponse(200)


"""
Service views, Use Case 4
"""


def search_for_question(content, contenttype, channelid, teamid, userid):
    if "?" in content:
        teamname = Team.objects.get(teamid=teamid).displayName
        message = f"""Hi all, I noticed that the students of team {teamname} asked a question in their teams. Maybe someone can help?: 
                    <br> <br>
        """
        name = User.objects.get(userid=userid).displayName
        message_end = "<br> <br> Kind Regards <br> Hermie"
        messageHandler.send_channel_message(
            "Frage der Studenten", message + name + ": " + content + message_end, e_tutoren_id, channel_id_etutors)
