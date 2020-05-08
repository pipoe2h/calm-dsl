jwt = '@@{calm_jwt}@@'
vm_name = '@@{calm_application_name}@@-app-move-vApp'

### Get VM
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

uri = 'https://localhost:9440/api/nutanix/v3'
action = 'search'

api_url = "/".join([uri, action])

payload = {
    "user_query": "\"Vm Name\"={}".format(vm_name),
    "explicit_query": True,
    "generate_autocompletions_only": True,
    "query_term_list": []
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    vm_uuid = resp['query_term_list'][0]['token_list'][0]['identifier']['value']
else:
    print("Post request failed", r.content)
    exit(1)

### Get VM IP Address
action = 'vms'

api_url = "/".join([uri, action, vm_uuid])

r = urlreq(api_url, verb='GET', headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    vm_ip = resp['status']['resources']['nic_list'][0]['ip_endpoint_list'][0]['ip']
    print("MOVE_VAPP_IP={}".format(vm_ip))
else:
    print("Post request failed", r.content)
    exit(1)
