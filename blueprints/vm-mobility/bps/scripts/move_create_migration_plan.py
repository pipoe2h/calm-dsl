#script
move_ip = '@@{address}@@'
move_password = '@@{Cred_Move.secret}@@'

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
                "TargetNetworkID": Move_AHV_Network,
                "TestNetworkID": ""
            }
        ],
        "Workload": {
            "Type": "VM",
            "VMs": [
                {
                    "AllowUVMOps": False,
                    "VMReference": {
                        "UUID": Move_AWS_VmUUID,
                        "VMID": Move_AWS_VmID
                    },
                    "GuestPrepMode": "manual",
                    "RetainMacAddress": True,
                    "PowerOffForpRDMtovRDMConversion": True
                }
            ]
        }
    }
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp['Status']['State'])

else:
    print("Get request failed", r.content)
    exit(1)