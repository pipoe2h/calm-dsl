move_ip = '@@{MOVE_VAPP_IP}@@'
move_password = '@@{Cred_PC.secret}@@'
AWS_ACCESS_KEY = '@@{Cred_AWS.username}@@'
AWS_SECRET_KEY = '@@{Cred_AWS.secret}@@'
PC_ADMIN = '@@{Cred_PC.username}@@'
PC_PASSWORD = '@@{Cred_PC.secret}@@'
PC_IP = '@@{PC_IP}@@'

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

sleep(60)

# Create AWS Provider
api_url = 'https://{}/move/v2/providers'.format(move_ip)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Spec": {
        "Name": "Calm AWS Demo",
        "AWSAccessInfo": {
            "AccessKey": AWS_ACCESS_KEY,
            "SecretKey": AWS_SECRET_KEY
        },
        "Type": "AWS"
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    move_aws_provideruuid = resp['MetaData']['UUID']
    print(resp['Status']['State'])

else:
    print("Get request failed", r.content)
    exit(1)

# Create AHV Provider
api_url = 'https://{}/move/v2/providers'.format(move_ip)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Spec": {
        "Name": "Calm AHV Demo",
        "AOSAccessInfo": {
            "IPorFQDN": PC_IP,
            "Password": PC_PASSWORD,
            "Username": PC_ADMIN
        },
        "Type": "AOS"
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    move_ahv_provideruuid = resp['MetaData']['UUID']
    print(resp['Status']['State'])

else:
    print("Get request failed", r.content)
    exit(1)

print("MOVE_AWS_PROVIDERUUID={}".format(move_aws_provideruuid))
print("MOVE_AHV_PROVIDERUUID={}".format(move_ahv_provideruuid))