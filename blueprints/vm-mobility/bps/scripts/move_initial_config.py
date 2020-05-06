#script
move_ip = '@@{address}@@'
move_new_password = '@@{Cred_Move.secret}@@'

# Get auth token
api_url = 'https://{}/move/v2/users/login'.format(move_ip)
headers = {'Content-Type': 'application/json',  'Accept':'application/json'}

payload = {
    "Spec": {
        "Password": "nutanix/4u", 
        "UserName": "nutanix"
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    move_token = resp['Status']['Token']
else:
    print("Get request failed", r.content)
    exit(1)

# Accept EULA and Set password
api_url = 'https://{}/move/v2/configure'.format(move_ip)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Spec": {
        "EulaAccepted": True,
        "TelemetryOn": True,
        "NewPassword": move_new_password
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    print(r.status_code)

else:
    print("Get request failed", r.content)
    exit(1)