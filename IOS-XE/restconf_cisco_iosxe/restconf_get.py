import requests
import json
from pprint import pprint


#VARIABLES
IP = "172.16.255.41"
PORT = "443"
USER = "cisco"
PASSWORD = "cisco"

# connection parameters
router = {
    "ip": IP,
    "port": PORT,
    "user": USER,
    "password" : PASSWORD
}

# Headers
headers = {
    "Accept" : "application/yang-data+json",
    "Content=Type" : "application/yang-data+json"
}

#URL
URL = f"https://{router['ip']}:{router['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/"

# Perform GET request

response = requests.get(
    URL,
    headers = headers,
    auth = (router['user'], router['password']), 
    verify=False
)

# Convert JSON response to Python DICT
data = response.json()

# Show the interface name and status per interface
print("*" * 40)
print('INTERFACE NAME  |  STATUS')
for interface in data["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
    print("{} | {}".format(interface['name'],interface['admin-status']))
    


