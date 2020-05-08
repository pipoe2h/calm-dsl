move_ip = '@@{Move_IP}@@'
move_password = '@@{Cred_Move.secret}@@'
vm_name = '@@{name}@@'
Move_AWS_Region = '@@{awsRegion}@@'
Move_AWS_ProviderUUID = '@@{moveAwsProviderUuid}@@'

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

# Create EC2
api_url = 'https://{}/move/v2/providers/{}/workloads/list'.format(move_ip,Move_AWS_ProviderUUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Filter": {
        "Datacenter": [
            Move_AWS_Region
        ]
    },
    "ShowVMS": "all",
    "SortBy": "VMName",
    "SortOrderDesc": False,
    "Query": vm_name,
    "Limit": 1,
    "RefreshInventory": True
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    awsVmUuid = resp['Entities'][0]['VMUuid']
    awsVmId = resp['Entities'][0]['VmID']
else:
    print("Get request failed", r.content)
    exit(1)

print("MOVE_AWS_VM_UUID".format(awsVmUuid))
print("MOVE_AWS_VM_ID".format(awsVmId))