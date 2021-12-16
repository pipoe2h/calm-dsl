jwt = "@@{calm_jwt}@@"
vm_uuid = "@@{id}@@"
new_disk_size = "@@{ROOT_DISK_SIZE}@@"

api_url = "https://localhost:9440/api/nutanix/v3/vms/{}".format(vm_uuid)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

r = urlreq(api_url, verb='GET', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    del resp['status']
    resp['spec']['resources']['disk_list'][0]['disk_size_mib'] = int(new_disk_size)*1024
else:
    print("Get request failed", r.content)
    exit(1)

r = urlreq(api_url, verb='PUT', params=json.dumps(resp), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print("Root partition extended to: {} GB".format(resp['spec']['resources']['disk_list'][0]['disk_size_mib']/1024))
else:
    print("Get request failed", r.content)
    exit(1)