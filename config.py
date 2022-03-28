from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("config.ini")

api_server = config_object["APISERVER"]  
client_registration = config_object["CLIENT_REGISTRATION"]
group_assignment = config_object["GROUP_ASSIGNMENT"]