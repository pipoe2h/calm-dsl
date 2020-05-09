move_ip = '@@{Move_IP}@@'
move_password = '@@{Cred_Move.secret}@@'
Move_PlanUUID = '@@{MOVE_PLANUUID}@@'
Move_AWS_VmUUID = '@@{MOVE_AWS_VM_UUID}@@'

# Get auth token
api_url = 'https://{}/move/v2/users/login'.format(move_ip)
headers = {'Content-Type': 'application/json',  'Accept':'application/json'}

payload = {
    "Spec": {
        "Password": move_password, 
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

# Cutover Migration Plan
api_url = 'https://{}/move/v2/plans/{}/workloads/{}/action'.format(move_ip,Move_PlanUUID,Move_AWS_VmUUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Spec": {
        "Action": "cutover"
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    
    while "DELETE" not in resp['Status']['Actions']:
        r = urlreq(api_url, verb='POST', headers=headers, verify=False)

        if r.ok:
            resp = json.loads(r.content)
            sleep(30)
        else:
            print("Request failed", r.content)
            exit(1)

    print("Migration completed")

else:
    print("Request failed", r.content)
    exit(1)