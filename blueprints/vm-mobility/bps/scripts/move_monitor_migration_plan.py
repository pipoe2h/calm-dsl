move_ip = '@@{Move_IP}@@'
move_password = '@@{Cred_Move.secret}@@'
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
    
# Monitor Migration Plan
api_url = 'https://{}/move/v2/plans/{}/workloads/list'.format(move_ip,Move_PlanUUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

r = urlreq(api_url, verb='POST', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    print("========MONITOR========")
    print(r.content)
    
    while "Progress" not in resp['Status']['VMStatus'][0]:

        print("========PROGRESS========")
        print(r.content)

        if "DELETE" in resp['Status']['Actions'][0]:
            print(resp['Status']['VMStatus'][0]['ErrorMessage'])
            exit(1)

        r = urlreq(api_url, verb='POST', headers=headers, verify=False)

        if r.ok:
            resp = json.loads(r.content)
            sleep(5)
        else:
            print("Request failed", r.content)
            exit(1)

    while resp['Status']['VMStatus'][0]['Progress'] != 100:

        print("========100========")
        print(r.content)

        r = urlreq(api_url, verb='POST', headers=headers, verify=False)

        if r.ok:
            resp = json.loads(r.content)
            print("Progress: {}%".format(resp['Status']['VMStatus'][0]['ProgressPercentage']))
            sleep(30)
        else:
            print("Request failed", r.content)
            exit(1)

    while "CUTOVER" not in resp['Status']['VMStatus'][0]['Actions']:

        print("========CUTOVER========")
        print(r.content)

        r = urlreq(api_url, verb='POST', headers=headers, verify=False)

        if r.ok:
            resp = json.loads(r.content)
            sleep(5)
        else:
            print("Request failed", r.content)
            exit(1)

else:
    print("Request failed", r.content)
    exit(1)