jwt = '@@{calm_jwt}@@'
pc_ip = 'localhost'
vm_name = '@@{name}@@'
project_name = '@@{calm_project_name}@@'
ahv_vm_id = '@@{AHV_VM_UUID}@@'
username = '@@{Cred_OS.username}@@'
password = '@@{Cred_OS.secret}@@'


BP_SPEC = {
    "api_version": "3.0",
    "metadata": {
        "kind": "blueprint",
        "categories": {},
        "project_reference": {
            "kind": "project",
            "uuid": ""
        },
        "uuid": "00000000-0000-0000-0000-000000000000"
    },
    "spec": {
        "resources": {
            "service_definition_list": [
                {
                    "name": "Linux",
                    "depends_on_list": [],
                    "variable_list": [],
                    "port_list": [],
                    "action_list": [],
                    "uuid": "11111111-1111-1111-1111-111111111111"
                }
            ],
            "credential_definition_list": [
                {
                    "name": "Cred_OS",
                    "type": "PASSWORD",
                    "username": username,
                    "secret": {
                        "attrs": {
                            "is_secret_modified": True
                        },
                        "value": password
                    },
                    "uuid": "22222222-2222-2222-2222-222222222222"
                }
            ],
            "substrate_definition_list": [
                {
                    "variable_list": [],
                    "type": "AHV_VM",
                    "os_type": "Linux",
                    "action_list": [],
                    "create_spec": {
                        "name": "VM",
                        "resources": {
                            "disk_list": [
                                {
                                    "data_source_reference": {},
                                    "device_properties": {
                                        "device_type": "DISK",
                                        "disk_address": {
                                            "device_index": 0,
                                            "adapter_type": "SCSI"
                                        }
                                    }
                                }
                            ],
                            "nic_list": [],
                            "boot_config": {
                                "boot_device": {
                                    "disk_address": {
                                        "device_index": 0,
                                        "adapter_type": "SCSI"
                                    }
                                }
                            },
                            "account_uuid": ""
                        },
                        "categories": {}
                    },
                    "name": "VM",
                    "readiness_probe": {
                        "connection_type": "SSH",
                        "connection_port": 22,
                        "connection_protocol": "",
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
                    "uuid": "44444444-4444-4444-4444-444444444444"
                }
            ],
            "default_credential_local_reference": {
                "kind": "app_credential",
                "name": "default_credential",
                "uuid": "22222222-2222-2222-2222-222222222222"
            },
            "published_service_definition_list": [],
            "package_definition_list": [
                {
                    "type": "DEB",
                    "variable_list": [],
                    "options": {
                        "install_runbook": {
                            "name": "1cc36442_runbook",
                            "variable_list": [],
                            "main_task_local_reference": {
                                "kind": "app_task",
                                "uuid": "55555555-5555-5555-5555-555555555555"
                            },
                            "task_definition_list": [
                                {
                                    "name": "681c6689_dag",
                                    "target_any_local_reference": {
                                        "kind": "app_package",
                                        "uuid": "66666666-6666-6666-6666-666666666666"
                                    },
                                    "variable_list": [],
                                    "child_tasks_local_reference_list": [],
                                    "type": "DAG",
                                    "attrs": {
                                        "edges": []
                                    },
                                    "uuid": "55555555-5555-5555-5555-555555555555"
                                }
                            ],
                            "uuid": "77777777-7777-7777-7777-777777777777"
                        },
                        "uninstall_runbook": {
                            "name": "dde4e89f_runbook",
                            "variable_list": [],
                            "main_task_local_reference": {
                                "kind": "app_task",
                                "uuid": "88888888-8888-8888-8888-888888888888"
                            },
                            "task_definition_list": [
                                {
                                    "name": "79d8117f_dag",
                                    "target_any_local_reference": {
                                        "kind": "app_package",
                                        "uuid": "66666666-6666-6666-6666-666666666666"
                                    },
                                    "variable_list": [],
                                    "child_tasks_local_reference_list": [],
                                    "type": "DAG",
                                    "attrs": {
                                        "edges": []
                                    },
                                    "uuid": "88888888-8888-8888-8888-888888888888"
                                }
                            ],
                            "uuid": "99999999-9999-9999-9999-999999999999"
                        }
                    },
                    "service_local_reference_list": [
                        {
                            "kind": "app_service",
                            "uuid": "11111111-1111-1111-1111-111111111111"
                        }
                    ],
                    "name": "Package1",
                    "uuid": "66666666-6666-6666-6666-666666666666"
                }
            ],
            "app_profile_list": [
                {
                    "name": "Default",
                    "action_list": [],
                    "variable_list": [],
                    "deployment_create_list": [
                        {
                            "variable_list": [],
                            "action_list": [],
                            "min_replicas": "1",
                            "name": "afdddecd_deployment",
                            "brownfield_instance_list": [
                                {
                                    "instance_id": "",
                                    "instance_name": "",
                                    "address": [],
                                    "platform_data": {}
                                }
                            ],
                            "max_replicas": "1",
                            "substrate_local_reference": {
                                "kind": "app_substrate",
                                "uuid": "44444444-4444-4444-4444-444444444444"
                            },
                            "default_replicas": "1",
                            "type": "BROWNFIELD",
                            "package_local_reference_list": [
                                {
                                    "kind": "app_package",
                                    "uuid": "66666666-6666-6666-6666-666666666666"
                                }
                            ],
                            "uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                        }
                    ],
                    "uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
                }
            ],
            "type": "BROWNFIELD"
        },
        "name": "",
        "description": "* [WebApp](http://@{}@)".format("@{Linux.address}@")
    }
}

    ### --------------------------------------------------------------------------------- ###


def ahv_single_vm_run(spec):

    headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}
    base_url = "https://{}:9440/api/nutanix/v3".format(pc_ip)

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
    def get_project_uuid(base_url, project_name):

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
    def get_ahv_account_uuid(base_url, account_name):
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
    def get_ahv_vm(base_url, vm_id):
        method = 'GET'
        url = base_url + "/vms/{}".format(vm_id)

        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            headers=headers,
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
    def create_single_vm_bp(base_url, payload):

        method = 'POST'
        url = base_url + "/blueprints"
        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            params=json.dumps(payload),
            headers=headers,
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
    def launch_single_vm_bp(base_url, blueprint_uuid, payload):

        method = 'POST'
        url = base_url + "/blueprints/{}/launch".format(blueprint_uuid)
        print("Making a {} API call to {}".format(method, url))
        resp = urlreq(
            url,
            verb=method,
            params=json.dumps(payload),
            headers=headers,
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
    project_uuid = get_project_uuid(base_url, project_name)
    ahv_account_name, ahv_vm_ip = get_ahv_vm(base_url, ahv_vm_id)
    account_uuid = get_ahv_account_uuid(base_url, ahv_account_name)

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
    resp = create_single_vm_bp(base_url, updated_spec)

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
    launch_single_vm_bp(base_url, blueprint_uuid, resp)


ahv_single_vm_run(BP_SPEC)