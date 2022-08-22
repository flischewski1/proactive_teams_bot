import requests
import json

# load relevant variables

config = json.load(open("import_credentials.json", "r"))

url_channels = config["BOTURL_Channel"]
url_users = config["BOTURL_Users"]


headers = {
  'Content-Type': 'application/json'
}

# message to teamschannel
def send_channel_message(subject,body,teams_id,channel_id): 
    message_dict = {
        "subject":subject,
        "body":body,
        "teams-id":teams_id,
        "channel-id":channel_id
    }
    try:
        requests.request("POST", url_channels, headers=headers, data=json.dumps(message_dict))
        return True
    except:
        return False

# message to user
def send_user_message(body,user_id): 
    message_dict = {
        "user-id":user_id,
        "body":body
    }
    try:
        requests.request("POST", url_users, headers=headers, data=json.dumps(message_dict))
        return True
    except:
        return False


