move_ip = '@@{Move_IP}@@'
move_password = '@@{Cred_Move.secret}@@'
Move_AHV_ClusterUUID = '@@{peUuid}@@'
Move_AHV_ContainerUUID = '@@{scUuid}@@'
Move_AHV_NetworkUuid = '@@{ahvNetworkUuid}@@'
Move_AWS_Vpc = '@@{awsVpcId}@@'
Move_AWS_Region = '@@{awsRegion}@@'
Move_AWS_ProviderUUID = '@@{moveAwsProviderUuid}@@'
Move_AHV_ProviderUUID = '@@{moveAhvProviderUuid}@@'
Move_AWS_VmUUID = '@@{MOVE_AWS_VM_UUID}@@'
Move_AWS_VmID = '@@{MOVE_AWS_VM_ID}@@'

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

# Create Migration Plan
api_url = 'https://{}/move/v2/plans'.format(move_ip)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': '{}'.format(move_token)}

payload = {
    "Spec": {
        "Name": "Calm Workload Mobility Demo",
        "SourceInfo": {
            "ProviderUUID": Move_AWS_ProviderUUID,
            "AWSProviderAttrs": {
                "RegionID": Move_AWS_Region
            }
        },
        "TargetInfo": {
            "ProviderUUID": Move_AHV_ProviderUUID,
            "AOSProviderAttrs": {
                "ClusterUUID": Move_AHV_ClusterUUID,
                "ContainerUUID": Move_AHV_ContainerUUID
            }
        },
        "NetworkMappings": [
            {
                "SourceNetworkID": Move_AWS_Vpc,
                "TargetNetworkID": Move_AHV_NetworkUuid,
                "TestNetworkID": ""
            }
        ],
        "Settings": {
            "GuestPrepMode": "auto"
        },
        "Workload": {
            "Type": "VM",
            "VMs": [
                {
                    "AllowUVMOps": True,
                    "RetainMacAddress": False,
                    "VMReference": {
                        "UUID": Move_AWS_VmUUID,
                        "VMID": Move_AWS_VmID
                    }
                }
            ]
        }
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    planUuid = resp['MetaData']['UUID']
else:
    print("Get request failed", r.content)
    exit(1)

print("MOVE_PLANUUID={}".format(planUuid))