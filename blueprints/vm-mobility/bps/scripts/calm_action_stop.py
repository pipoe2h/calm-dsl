jwt = '@@{calm_jwt}@@'
pc_ip = 'localhost'
App_UUID = '@@{calm_application_uuid}@@'

# Stop VM
api_url = 'https://{}:9440/api/nutanix/v3/apps/{}/actions/run'.format(pc_ip,App_UUID)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

payload = {
    "name": "action_stop"
}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)
if r.ok:
    resp = json.loads(r.content)
    runlog_uuid = resp['runlog_uuid']

else:
    print("Request failed", r.content)
    exit(1)

# # Monitor VM Stop
# api_url = 'https://{}:9440/api/nutanix/v3/apps/{}/app_runlogs/{}/output'.format(pc_ip,App_UUID,runlog_uuid)
# headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

# r = urlreq(api_url, verb='GET', headers=headers, verify=False)
# if r.ok:
#     resp = json.loads(r.content)
    
#     while resp['status']['runlog_state'] != "SUCCESS":
#         if resp['status']['runlog_state'] == "FAILED":
#             print("Task failed, please check in Calm")
#             exit(1)

#         r = urlreq(api_url, verb='GET', headers=headers, verify=False)
#         resp = json.loads(r.content)
#         sleep(10)

#     print("VM powered off")

# else:
#     print("Request failed", r.content)
#     exit(1)
