pc_ip = 'localhost'
vm_name = '@@{vm_name}@@'
project_name = '@@{project_name}@@'
ahv_vm_id = '@@{vm_uuid}@@'
pc_user = '@@{Cred_PC.username}@@'
pc_password = '@@{Cred_PC.secret}@@'


BP_SPEC = {
    "api_version": "3.0",
    "metadata": {
      "kind": "blueprint",
      "categories": {
          "TemplateType": "Vm"
      },
      "project_reference": {
        "kind": "project",
        "uuid": ""
      },
      "uuid": "67ff4eaf-f7e3-4563-b1da-f42de3113402"
    },
    "spec": {
      "resources": {
        "substrate_definition_list": [
          {
            "variable_list": [],
            "type": "AHV_VM",
            "os_type": "Linux",
            "action_list": [],
            "create_spec": {
              "type": "",
              "name": "vm-@@{calm_time}@@",
              "resources": {
                "account_uuid": "",
                "num_vcpus_per_socket": 0,
                "num_sockets": 0,
                "memory_size_mib": 0,
                "nic_list": []
              },
              "availability_zone_reference": None,
              "backup_policy": None,
              "cluster_reference": None,
              "categories": {}
            },
            "name": "VMSubstrate",
            "readiness_probe": {
              "disable_readiness_probe": True
            },
            "editables": {
              "create_spec": {
                "resources": {
                  "nic_list": {},
                  "serial_port_list": {}
                }
              }
            },
            "uuid": "61520e7a-67cc-e521-2853-fe249c92de18"
          }
        ],
        "client_attrs": {},
        "app_profile_list": [
          {
            "name": "VMware",
            "action_list": [],
            "variable_list": [],
            "deployment_create_list": [
              {
                "variable_list": [],
                "action_list": [],
                "min_replicas": "1",
                "name": "a7aadef7_deployment",
                "brownfield_instance_list": [
                  {
                    "instance_id": "",
                    "instance_name": "",
                    "address": [
                    ],
                    "platform_data": {}
                  }
                ],
                "max_replicas": "1",
                "substrate_local_reference": {
                  "kind": "app_substrate",
                  "uuid": "61520e7a-67cc-e521-2853-fe249c92de18"
                },
                "type": "BROWNFIELD",
                "uuid": "48a70045-d71a-4486-0d03-e15a871372b5"
              }
            ],
            "uuid": "bc40ba37-6e84-49af-1ad3-280a5c3c1af4"
          }
        ],
        "type": "BROWNFIELD"
      },
      "name": ""
    }
}

    ### --------------------------------------------------------------------------------- ###


def ahv_single_vm_run(spec):

    headers = {'Content-Type': 'application/json',  'Accept':'application/json'}
    base_url = "https://{}:9440/api/nutanix/v3".format(pc_ip)
    auth = { "username": pc_user, "password": pc_password}

    ### --------------------------------------------------------------------------------- ###
    def change_uuids(bp, context):
        """
        Helper function to change uuids
        Args:
            bp (dict): BP dict
            context (dict) : context to recursively change uuid references
        """
        if isinstance(bp, dict):
            for key, val in bp.iteritems():
                if key == 'uuid':
                    old_uuid = val
                    if old_uuid in context:
                        bp[key] = context[old_uuid]
                    else:
                        new_uuid = str(uuid.uuid4())
                        context[old_uuid] = new_uuid
                        bp[key] = new_uuid
                else:
                    change_uuids(val, context)
        elif isinstance(bp, list):
            for item in bp:
                if isinstance(item, str):
                    try:
                        uuid.UUID(hex=str(item), version=4)
                    except Exception:
                        change_uuids(item, context)
                        continue
                    old_uuid = item
                    if old_uuid in context:
                        new_uuid = context[old_uuid]
                        bp[bp.index(item)] = new_uuid
                    else:
                        new_uuid = str(uuid.uuid4())
                        context[old_uuid] = new_uuid
                        bp[bp.index(item)] = new_uuid
                else:
                    change_uuids(item, context)
        return bp
    ### --------------------------------------------------------------------------------- ###

    ### --------------------------------------------------------------------------------- ###
    def get_project_uuid(base_url, auth, project_name):

        method = 'POST'
        url = base_url + "/projects/list"
        payload = {
            "length":100,
            "offset":0,
            "filter":"name=={0}".format(project_name)
        }
        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            params=json.dumps(payload),
            headers=headers,
            auth='BASIC',
            user=auth["username"],
            passwd=auth["password"],
            verify=False
        )

        if resp.ok:
            json_resp = json.loads(resp.content)
            if json_resp['metadata']['total_matches'] > 0:
                project = json_resp['entities'][0]
                return project["metadata"]["uuid"]
            else:
                print("Could not find project")
                exit(1)
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
    ### --------------------------------------------------------------------------------- ###

    ### --------------------------------------------------------------------------------- ###
    def get_ahv_account_uuid(base_url, auth, account_name):
        method = 'POST'
        url = base_url + "/accounts/list"
        payload = {
            "length":100,
            "offset":0,
            "filter":"name=={0};type==nutanix".format(account_name)
        }
        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            params=json.dumps(payload),
            headers=headers,
            auth='BASIC',
            user=auth["username"],
            passwd=auth["password"],
            verify=False
        )

        if resp.ok:
            json_resp = json.loads(resp.content)
            if json_resp['metadata']['total_matches'] > 0:
                account = json_resp['entities'][0]
                return account["metadata"]["uuid"]
            else:
                print("Could not find account")
                exit(1)
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
    ### --------------------------------------------------------------------------------- ###

    ### --------------------------------------------------------------------------------- ###
    def get_ahv_vm(base_url, auth, vm_id):
        method = 'GET'
        url = base_url + "/vms/{}".format(vm_id)

        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            headers=headers,
            auth='BASIC',
            user=auth["username"],
            passwd=auth["password"],
            verify=False
        )

        if resp.ok:
            json_resp = json.loads(resp.content)
            vm_ip = json_resp['spec']['resources']['nic_list'][0]['ip_endpoint_list'][0]['ip']
            cluster_name = json_resp['spec']['cluster_reference']['name']
            return cluster_name, vm_ip
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
    ### --------------------------------------------------------------------------------- ###

    ### --------------------------------------------------------------------------------- ###
    def create_single_vm_bp(base_url, auth, payload):

        method = 'POST'
        url = base_url + "/blueprints"
        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            params=json.dumps(payload),
            headers=headers,
            auth='BASIC',
            user=auth["username"],
            passwd=auth["password"],
            verify=False
        )

        if resp.ok:
            json_resp = json.loads(resp.content)
            if json_resp["status"]["state"] != "ACTIVE":
                print("Blueprint state is not Active. It is : {}".format(json_resp["status"]["state"]))
                print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
                exit(1)
            return json_resp
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
    ### --------------------------------------------------------------------------------- ###

    ### --------------------------------------------------------------------------------- ###
    def launch_single_vm_bp(base_url, auth, blueprint_uuid, payload):

        method = 'POST'
        url = base_url + "/blueprints/{}/launch".format(blueprint_uuid)
        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            params=json.dumps(payload),
            headers=headers,
            auth='BASIC',
            user=auth["username"],
            passwd=auth["password"],
            verify=False
        )

        if resp.ok:
            json_resp = json.loads(resp.content)
            print("Single VM Blueprint launched successfully")
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
    ### --------------------------------------------------------------------------------- ###

    ### Get project and account uuid
    project_uuid = get_project_uuid(base_url, auth, project_name)
    ahv_account_name, ahv_vm_ip = get_ahv_vm(base_url, auth, ahv_vm_id)
    account_uuid = get_ahv_account_uuid(base_url, auth, ahv_account_name)

    brownfield_instance_list = []
    vm_info = {
        "instance_name": vm_name,
        "instance_id": ahv_vm_id,
        "address": [
            ahv_vm_ip
        ],
        "platform_data": {}
    }
    brownfield_instance_list.append(vm_info)

    bp_name = "move-demo-{}".format(ahv_vm_ip.replace(".", "-"))

    ### Update uuids, project ref, account ref, bp name, vm-info etc.
    updated_spec = change_uuids(spec, {})
    updated_spec["metadata"]["project_reference"]["uuid"] = project_uuid
    substrate = updated_spec["spec"]["resources"]["substrate_definition_list"][0]

    substrate["create_spec"]["name"] = vm_name
    substrate["create_spec"]["resources"]["account_uuid"] = account_uuid

    updated_spec["spec"]["resources"]["substrate_definition_list"][0] = substrate
    updated_spec["spec"]["name"] = bp_name
    updated_spec["spec"]["resources"]["app_profile_list"][0]["deployment_create_list"][0]["brownfield_instance_list"] = brownfield_instance_list

    print(updated_spec)
    ### Create a single vm bp
    resp = create_single_vm_bp(base_url, auth, updated_spec)

    ### Update single vm bp spec
    del resp["status"]
    blueprint_uuid = resp["metadata"]["uuid"]

    app_uuid = resp["spec"]["resources"]["app_profile_list"][0]["uuid"]
    resp["spec"]["application_name"] =  resp["spec"]["name"]
    resp["spec"]["app_profile_reference"] = {
        "kind": "app_profile",
        "uuid": app_uuid
    }

    del resp["spec"]["name"]

    ### Launch a single vm bp
    launch_single_vm_bp(base_url, auth, blueprint_uuid, resp)


ahv_single_vm_run(BP_SPEC)