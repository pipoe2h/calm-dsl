jwt = '@@{calm_jwt}@@'
vm_uuid = '@@{id}@@'
os_username = '@@{Centos.username}@@'
os_password = '@@{Centos.secret}@@'

api_url = 'https://localhost:9440/api/nutanix/v3/vms/{}'.format(vm_uuid)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}
r = urlreq(api_url, verb='GET', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)
else:
    print("Get request failed", r.content)
    exit(1)

ngt_install = {
    "nutanix_guest_tools": {
        "iso_mount_state": "MOUNTED",
        "state": "ENABLED",
        "ngt_state": "INSTALLED",
        "credentials": {
            "username": os_username,
            "password": os_password
        },
        "enabled_capability_list": []
    }
}

del resp['status']
resp['spec']['resources']['guest_tools'] = ngt_install

r = urlreq(api_url, verb='PUT', params=json.dumps(resp), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    print(resp)
else:
    print("Put request failed", r.content)
    exit(1)

task_status = resp['status']['state']
task_uuid = resp['status']['execution_context']['task_uuid']

api_url = 'https://localhost:9440/api/nutanix/v3/tasks/{}'.format(task_uuid)
while task_status != 'SUCCEEDED':

    r = urlreq(api_url, verb='GET', headers=headers, verify=False)
    if r.ok:
        resp = json.loads(r.content)
        task_status = resp['status']

        print('Percentage completed: {}'.format(resp['percentage_complete']))

        if task_status == 'SUCCEEDED':
            print('NGT Installed.')
            break
        elif task_status == 'ERROR':
            print('Task failed', resp['error_detail'])
            exit(1)
        else:
            sleep(10)
    else:
        print("Get request failed", r.content)
        exit(1)
