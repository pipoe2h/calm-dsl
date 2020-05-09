move_ip = '@@{Move_IP}@@'
move_password = '@@{Cred_Move.secret}@@'
Move_AWS_VmUUID = '@@{MOVE_AWS_VM_UUID}@@'
Move_PlanUUID = '@@{MOVE_PLANUUID}@@'

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

# Start Migration Plan
api_url = 'https://{}/move/v2/plans/{}/start'.format(move_ip,Move_PlanUUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

r = urlreq(api_url, verb='POST', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)        
else:
    print("Request failed", r.content)
    exit(1)

# # Monitor Migration Plan
# api_url = 'https://{}/move/v2/plans/{}/workloads/{}'.format(move_ip,Move_PlanUUID,Move_AWS_VmUUID)
# headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

# r = urlreq(api_url, verb='GET', headers=headers, verify=False)
# if r.ok:
#     resp = json.loads(r.content)
    
#     while "CUTOVER" not in resp['Status']['Actions']:
#         r = urlreq(api_url, verb='GET', headers=headers, verify=False)

#         sleep(120)


# else:
#     print("Request failed", r.content)
#     exit(1)