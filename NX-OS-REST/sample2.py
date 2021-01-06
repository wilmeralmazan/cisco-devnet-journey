import requests
import json
import re

#VARIABLES - UPDATE TO YOUR CREDENTIALS
USERNAME =  "cisco"
PASSWORD = "cisco"
IP = "172.16.255.51"


# GET THE LIST OF CDP NEIGHBORS USING API-CLI
URL = f"https://{IP}/ins"
myheader = {'content-type': 'application/json'}
payload = {
    'ins_api': {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show cdp neigh",  
        "output_format": "json"
    }
}

#MAKE POST REQUEST TO GET THE NEIGHTBORS TABLE AND CONVERT IT TO PYTHON DICT
CDP_RESPONSE = requests.post(URL, data=json.dumps(payload), headers=myheader, auth=(USERNAME, PASSWORD), verify=False).json()
#print(CDP_RESPONSE)


# CONTRUCT URL FOR REST LOGIN
AUTH_URL = f"https://{IP}/api/aaaLogin.json"

# CREATE PAYLOAD AS DICT
PAYLOAD= {
    "aaaUser": {
        "attributes": {
            "name": USERNAME,
            "pwd": PASSWORD
        }
    }
}

# PERFORM POST REQUEST TO AUTHENTICATE
AUTH_RESPONSE = requests.post(AUTH_URL, data=json.dumps(PAYLOAD), timeout=5, verify=False).json()

# GET AUTH TOKEN
TOKEN = AUTH_RESPONSE['imdata'][0]['aaaLogin']['attributes']['token']

# CREATE COOKIES
COOKIES = {}
COOKIES['APIC-cookie'] = TOKEN


# GET THE NUMBER OF CDP NEIGHBORS
NEIGH_COUNT = CDP_RESPONSE['ins_api']['outputs']['output']['body']['neigh_count']

# LOOP FOR EACH NEIGHBOR AND GET hostname, local interface and remote interface
for COUNTER in range(NEIGH_COUNT):
    hostname = CDP_RESPONSE["ins_api"]["outputs"]["output"]["body"]['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'][COUNTER]['device_id']
    local_int = CDP_RESPONSE["ins_api"]["outputs"]["output"]["body"]['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'][COUNTER]['intf_id']
    remote_int = CDP_RESPONSE["ins_api"]["outputs"]["output"]["body"]['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'][COUNTER]['port_id']
    body = {
        "l1PhysIf": {
            "attributes": {
                "descr": f"Connected to {hostname} .The remote interface is {remote_int}"
            }
        }
    }
    
    if local_int != "mgmt0":
        int_name = str.lower(str(local_int[:3]))
        int_num = re.search("[1-9]/[1-9]*", local_int)
        int_url = f"https://{IP}/api/mo/sys/intf/phys-[{int_name}" + str(int_num.group(0))+"].json"
        
        post_response = requests.post(int_url, data=json.dumps(body), headers=myheader,cookies = COOKIES, verify=False).json()
        print(post_response)