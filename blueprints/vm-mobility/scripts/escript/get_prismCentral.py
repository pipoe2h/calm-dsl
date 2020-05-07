#script
jwt = '@@{calm_jwt}@@'

# Get PC IP and PE uuid
api_url = 'https://localhost:9440/api/nutanix/v3/prism_central'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

r = urlreq(api_url, verb='GET', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    pc_ip = resp['resources']['pc_vm_list'][0]['nic_list'][0]['ip_list'][0]
    pe_uuid= resp['resources']['pc_vm_list'][0]['cluster_reference']['uuid']
    storage_container = resp['resources']['pc_vm_list'][0]['container_uuid']

else:
    print("Post request failed", r.content)
    exit(1)

print("PC_IP={}".format(pc_ip))
print("PE_UUID={}".format(pe_uuid))
print("SC_UUID={}".format(storage_container))
