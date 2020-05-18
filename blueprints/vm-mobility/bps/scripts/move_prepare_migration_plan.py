move_ip = '@@{Move_IP}@@'
move_password = '@@{Cred_Move.secret}@@'
Move_AWS_Region = '@@{awsRegion}@@'
Move_AWS_VmUUID = '@@{MOVE_AWS_VM_UUID}@@'
Move_PlanUUID = '@@{MOVE_PLANUUID}@@'
Os_Username = '@@{Cred_OS.username}@@'
Os_Password = '@@{Cred_OS.secret}@@'

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
    print("Request failed", r.content)
    exit(1)

# Prepare Migration Plan
api_url = 'https://{}/move/v2/plans/{}/prepare'.format(move_ip,Move_PlanUUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Spec": {
        "CommonCredentials": {
            "LinuxPassword": Os_Password,
            "LinuxUserName": Os_Username,
            "WindowsPassword": "",
            "WindowsUserName": "",
            "PemFile": ""
        },
        "Region": Move_AWS_Region,
        "VMs": [
            {
                "UserName": "",
                "Password": "",
                "UUID": Move_AWS_VmUUID,
                "GuestPrepMode": "auto"
            }
        ]
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    print("========PREPARE========")
    # print(r.content)

    while resp['Status']['Result']['Failed'] == None and resp['Status']['Result']['Passed'] == None:
        r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
        if r.ok:
            resp = json.loads(r.content)
            if "InstallationInProgress" in resp['Status']['Result']:
                print("Agent installation in progress...")
        else:
            print("Request failed", r.content)
            exit(1)
    
    if resp['Status']['Result']['Failed'] != None:
        print(resp['Status']['Result']['Failed'][0]['Message'])
        exit(1)
    else:
        print("Agent {}".format(resp['Status']['Result']['Passed'][0]['Status']))
        
else:
    print("Request failed", r.content)
    exit(1)

# Check Readiness
api_url = 'https://{}/move/v2/plans/{}/readiness'.format(move_ip,Move_PlanUUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

r = urlreq(api_url, verb='POST', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    print("========READINESS========")
    # print(r.content)
    
    if resp['Status']['Failed'] != None or resp['Status']['VMChecksResult']['Failed'] != None:
        print(resp['Status']['Failed'])
        print(resp['Status']['VMChecksResult']['Failed'])
        exit(1)
    else:
        print("VM ready for migration")
        
else:
    print("Request failed", r.content)
    exit(1)

