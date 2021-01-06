import requests
from pprint import pprint
import json

# VARIABLES
IP = "172.16.255.51"
USERNAME = "cisco"
PASSWORD = "cisco"

# Construct URL
URL = f"https://{IP}/api/aaaLogin.json"
nl = '\n'
nr = '\r'

#Create payload and then convert it to JSON object
payload= {
    "aaaUser": {
        "attributes": {
            "name": USERNAME,
            "pwd": PASSWORD
        }
    }
}

payload = json.dumps(payload)


# Create Headers
headers = {
  'Content-Type': 'application/json',
  'Accept': "*/*"
}

# Make request
response = requests.post(URL, headers=headers, data=payload, verify=False).json()


# Get Token
TOKEN = response['imdata'][0]['aaaLogin']['attributes']['token']

#print(TOKEN)

COOKIES = {}
COOKIES['APIC-cookie'] = TOKEN


URL = f"https://{IP}/api/node/mo/sys/intf/phys-[eth1/1].json"

payload="{\r\n    \"l1PhysIf\":{\r\n        \"attributes\":{\r\n            \"descr\": \"Changed by Mime and Melanie\"\r\n        }\r\n    }\r\n}"
headers = {
  'Content-Type': 'application/json',
}

#Excute the methid PUT to change the description in the interface Eth1/1
requests.put(URL, headers=headers, data=payload, cookies=COOKIES, verify=False).json()

