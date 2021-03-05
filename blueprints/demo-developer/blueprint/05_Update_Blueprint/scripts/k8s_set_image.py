#Variables used in this script 
KUBERNETES_CLUSTER_IP="@@{KUBERNETES_CLUSTER_IP}@@"
KUBERNETES_CLUSTER_PORT="@@{KUBERNETES_CLUSTER_PORT}@@"
KUBERNETES_CLUSTER_VERIFY_SSL=@@{KUBERNETES_CLUSTER_VERIFY_SSL}@@
KUBERNETES_API_KEY="@@{CRED_K8S.secret}@@"
KUBERNETES_NAMESPACE_NAME="@@{KUBERNETES_NAMESPACE_NAME}@@"
KUBERNETES_DEPLOYMENT_NAME="@@{calm_application_name}@@"
KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE="@@{KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE}@@"



import kubernetes.client
from kubernetes.client.rest import ApiException

# Configure API key authorization: BearerToken
configuration = kubernetes.client.Configuration()
configuration.host="https://%s:%s" %(KUBERNETES_CLUSTER_IP,KUBERNETES_CLUSTER_PORT)
configuration.verify_ssl=KUBERNETES_CLUSTER_VERIFY_SSL
configuration.api_key['authorization'] = "%s" %(KUBERNETES_API_KEY)
configuration.api_key_prefix['authorization'] = 'Bearer'


    
# Enter a context with an instance of the API kubernetes.client
with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kubernetes.client.AppsV1Api(api_client)
    name = KUBERNETES_DEPLOYMENT_NAME
    namespace = KUBERNETES_NAMESPACE_NAME
    body = {
    "spec": {
        "template": {
            "spec": {
                "containers": [
                    {
                        "image": KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE,
                        "name": "webpage"
                    }
                ]
            }
        }
    }
    }
    field_manager = 'nutanix-calm' # str | fieldManager is a name associated with the actor or entity that is making these changes. The value must be less than or 128 characters long, and only contain printable characters, as defined by https://golang.org/pkg/unicode/#IsPrint. This field is required for apply requests (application/apply-patch) but optional for non-apply patch types (JsonPatch, MergePatch, StrategicMergePatch). (optional)

    try:
        api_response = api_instance.patch_namespaced_deployment(name, namespace, body, field_manager=field_manager)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e)