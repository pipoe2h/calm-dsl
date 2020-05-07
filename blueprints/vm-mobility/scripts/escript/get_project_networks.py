#script
jwt = '@@{calm_jwt}@@'
project_name = '@@{calm_project_name}@@'

# Get project uuid
api_url = 'https://localhost:9440/api/nutanix/v3/projects/list'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

payload = {
    "filter": "name=={}".format(project_name)
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)

    networks = []
    for entity in resp['entities'][0]['spec']['resources']['subnet_reference_list']:
        networks.append(entity['name'])

    print(",".join(map(str,networks)))

else:
    print("Post request failed", r.content)
    exit(1)