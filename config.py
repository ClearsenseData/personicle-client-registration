from configparser import ConfigParser
import os

if os.environ.get("PRODUCTION","0")== "1":
    api_server = os.environ('API_SERVER')
    client_registration = os.environ('CLIENT_REGISTRATION')
    group_assignment_id = os.environ('GROUP_ASSIGNMENT_ID')
    group_assignment_endpoint= os.environ('GROUP_ASSIGNMENT_ENDPOINT')


else:
    config_object = ConfigParser()
    config_object.read("config.ini")

    api_server = config_object["APISERVER"]["TOKEN"]
    client_registration = config_object["CLIENT_REGISTRATION"]["ENDPOINT"]
    group_assignment_id = config_object["GROUP_ASSIGNMENT"]["GROUP_ID"]
    group_assignment_endpoint = config_object["GROUP_ASSIGNMENT"]["ENDPOINT"]