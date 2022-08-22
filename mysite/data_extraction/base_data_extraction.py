import json
import logging
from django.db import DataError
import requests
import msal


config = json.load(open("import_credentials.json", "r"))

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"],
    authority=config["authority"],
    client_credential=config["secret"])


def get_bearer_token():
    endpoint = config["endpoint_base"]
    token = None 
    token = app.acquire_token_silent(config["scope"], account=None)
    if not token:
        token = app.acquire_token_for_client(scopes=config["scope"])
    return token['access_token']

# get SharePoint URL for General folder
general_url = config["general_url"]
def check_upload(): 
    return import_data(general_url)

def import_data(endpoint_path):
    endpoint = config["endpoint_base"] + endpoint_path
    token = None
    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.
    token = app.acquire_token_silent(config["scope"], account=None)

    if not token:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        token = app.acquire_token_for_client(scopes=config["scope"])

    if "access_token" in token:
        next_page = ""
        # Calling graph using the access token
        graph_data = requests.get(
            endpoint,
            headers={'Authorization': 'Bearer ' + token['access_token']}, ).json()
        next_page = graph_data.get('@odata.nextLink', '')
        while next_page:
            additional_graph_data = requests.get(next_page,
                                                 headers={'Authorization': 'Bearer ' + token['access_token']}, ).json()
            next_page = additional_graph_data.get('@odata.nextLink', False)
            graph_data['value'] += additional_graph_data['value']
        try:
            return graph_data['value']
        except KeyError:
            return graph_data
    else:
        raise AssertionError("""Error: {error_name},
        Description: {error_description},
        Correlelation_id: {correlation_id}""".format(
            error_name=token.get("error"),
            error_description=token.get("error_description"),
            correlation_id=token.get("correlation_id")))


def import_sign_ins(): 
    endpoint_version = "beta"
    endpoint_root = "auditLogs"
    endpoint_type = "signIns"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root,endpoint_type])
    return import_data(endpoint_url)

def import_user_data():
    endpoint_version = "beta"
    endpoint_root = "users"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root])
    return import_data(endpoint_url)


def import_channel_data(team_id, channel_id):
    endpoint_version = "beta"
    endpoint_root = "teams"
    team_id = team_id
    subresource_type = "channels"
    subresource_id = channel_id
    information_type = "messages"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root, team_id, subresource_type, subresource_id, information_type])
    return import_data(endpoint_url)

def import_group_data(): 
    endpoint_version = "beta"
    endpoint_root = "groups"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root])
    return import_data(endpoint_url)


def import_member_data(team_id):
    endpoint_version = "beta"
    endpoint_root = "groups"
    team_id = team_id
    subresource_type = "members"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root, team_id, subresource_type])
    return import_data(endpoint_url)


def import_team_data(team_id):
    endpoint_version = "beta"
    endpoint_root = "teams"
    team_id = team_id
    subresource_type = "channels"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root, team_id, subresource_type])
    return import_data(endpoint_url)


def import_tenant_data():
    endpoint_version = "beta"
    endpoint_root = "groups"
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root])
    return import_data(endpoint_url)


def get_message(team_id, channel_id,message_id): 
    endpoint_version = "beta"
    endpoint_root = "teams"
    team_id = team_id
    subresource_type = "channels"
    channel_id = channel_id
    subsubresource_type = "messages"
    message_id=message_id
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root,team_id,subresource_type,channel_id,subsubresource_type,message_id])
    print(endpoint_url)
    return import_data(endpoint_url)

def get_reply(team_id, channel_id,message_id,reply_id): 
    endpoint_version = "beta"
    endpoint_root = "teams"
    team_id = team_id
    subresource_type = "channels"
    channel_id = channel_id
    subsubresource_type = "messages"
    message_id=message_id
    subsubsubresource_type = "replies"
    reply_id=reply_id
    endpoint_url = "/".join(
        [endpoint_version, endpoint_root,team_id,subresource_type,channel_id,subsubresource_type,message_id,subsubsubresource_type,reply_id])
    print(endpoint_url)
    return import_data(endpoint_url)

if __name__ == '__main__':
    print(check_upload())

    
            



