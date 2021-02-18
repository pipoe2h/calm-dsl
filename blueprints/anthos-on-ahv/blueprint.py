import os
import json

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint
from calm.dsl.builtins import action, ref, basic_cred, CalmTask
from calm.dsl.builtins import read_local_file, read_ahv_spec, read_vmw_spec, read_file
from calm.dsl.builtins import vm_disk_package
from calm.dsl.builtins import CalmVariable as Variable
from calm.dsl.builtins import read_env

# Credentials definition
OS_USERNAME = os.getenv("CALMDSL_OS_USERNAME") or read_local_file(
    os.path.join("secrets", "os_username")
)
OS_KEY = os.getenv("CALMDSL_OS_KEY") or read_local_file(
    os.path.join("secrets", "os_key")
)
CRED_OS = basic_cred(
    OS_USERNAME,
    OS_KEY,
    name="CRED_OS",
    type="KEY",
    default=True,
)

PE_USERNAME = os.getenv("CALMDSL_PE_USERNAME") or read_local_file(
    os.path.join("secrets", "pe_username")
)
PE_PASSWORD = os.getenv("CALMDSL_PE_PASSWORD") or read_local_file(
    os.path.join("secrets", "pe_password")
)
CRED_PE = basic_cred(
    PE_USERNAME,
    PE_PASSWORD,
    name="CRED_PE",
    type="PASSWORD",
    default=False,
)

GCLOUD_ACCOUNT = os.getenv("CALMDSL_GCLOUD_ACCOUNT") or read_local_file(
    os.path.join("secrets", "gcloud_account")
)
GCLOUD_KEY = os.getenv("CALMDSL_GCLOUD_KEY") or read_local_file(
    os.path.join("secrets", "gcloud_key")
)
CRED_GCLOUD = basic_cred(
    GCLOUD_ACCOUNT,
    GCLOUD_KEY,
    name="CRED_GCLOUD",
    type="KEY",
    default=False,
)

# Downloadable image for AHV
AHV_CENTOS = vm_disk_package(
    name="AHV_CENTOS", config_file="specs/image/centos-cloudimage.yaml"
)

# Anthos Control VMs Service
class ControlPlaneVMs(Service):

    """Control Plane VMs"""

    @action
    def Centos_Install_Docker():
        CalmTask.Exec.ssh(
            filename="scripts/centos_install_docker.sh",
            name="Install_Docker"
        )

    @action
    def NTNXPC_Extend_Disk():
        CalmTask.Exec.escript(
            filename="scripts/ntnxpc_extend_disk.py",
            name="Extend_OS_Disk"
        )


class ControlPlaneVMs_Package(Package):

    services = [ref(ControlPlaneVMs)]

    @action
    def __install__():
        ControlPlaneVMs.NTNXPC_Extend_Disk(name="NTNXPC_Extend_Disk")
        ControlPlaneVMs.Centos_Install_Docker(name="Centos_Install_Docker")


class ControlPlaneVMs_Substrate(Substrate):

    os_type = "Linux"
    
    provider_spec = read_ahv_spec(
        "specs/substrate/controlVm-spec.yaml",
        disk_packages={1: AHV_CENTOS}
    )
    provider_spec.spec["name"] = "@@{ANTHOS_CLUSTER_NAME}@@-anthos-controlVm-@@{calm_array_index}@@"

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(CRED_OS),
    }


class ControlPlaneVMs_Deployment(Deployment):

    min_replicas = "3"
    max_replicas = "3"

    packages = [ref(ControlPlaneVMs_Package)]
    substrate = ref(ControlPlaneVMs_Substrate)


# Anthos Worker VMs Service
class WorkerNodesVMs(Service):
    """Worker Nodes VMs"""

    @action
    def Centos_Install_Docker():
        CalmTask.Exec.ssh(
            filename="scripts/centos_install_docker.sh",
            name="Install_Docker"
        )

    @action
    def NTNXPC_Extend_Disk():
        CalmTask.Exec.escript(
            filename="scripts/ntnxpc_extend_disk.py",
            name="Extend_OS_Disk"
        )


class WorkerNodesVMs_Package(Package):

    services = [ref(WorkerNodesVMs)]

    @action
    def __install__():
        WorkerNodesVMs.NTNXPC_Extend_Disk(name="NTNXPC_Extend_Disk")
        WorkerNodesVMs.Centos_Install_Docker(name="Centos_Install_Docker")


class WorkerNodesVMs_Substrate(Substrate):

    os_type = "Linux"
    
    provider_spec = read_ahv_spec(
        "specs/substrate/workerVm-spec.yaml",
        disk_packages={1: AHV_CENTOS}
    )
    provider_spec.spec["name"] = "@@{ANTHOS_CLUSTER_NAME}@@-anthos-workerVm-@@{calm_array_index}@@"

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(CRED_OS),
    }


class WorkerNodesVMs_Deployment(Deployment):

    min_replicas = "2"
    max_replicas = "99"

    packages = [ref(WorkerNodesVMs_Package)]
    substrate = ref(WorkerNodesVMs_Substrate)


# Anthos Admin VM Service
class AdminVM(Service):
    """Admin VM"""

    dependencies = [
        ref(ControlPlaneVMs_Deployment),
        ref(WorkerNodesVMs_Deployment)
    ]

    @action
    def __create__():
        AdminVM.Anthos_Create_Cluster(name="Anthos_Create_Cluster")
        AdminVM.GKE_Configure_CloudConsole(name="GKE_Configure_CloudConsole")
        AdminVM.NTNXK8S_Install_CSI(name="NTNXK8S_Install_CSI")

    @action
    def Gcloud_Install_SDK():

        CalmTask.Exec.ssh(
            filename="scripts/gcloud_install_sdk.sh",
            name="Install_SDK"
        )
        CalmTask.SetVariable.ssh(
            filename="scripts/gcloud_configure_account.sh",
            name="Configure_Gcloud",
            variables=["GCP_PROJECT_ID","GCP_KEY"]
        )

    @action
    def Anthos_Install_CLI():
        CalmTask.Exec.ssh(
            filename="scripts/anthos_install_bmctl.sh",
            name="Install_CLI"
        )

    @action
    def Anthos_Create_Cluster():    
        CalmTask.SetVariable.ssh(
            filename="scripts/anthos_create_cluster.sh",
            name="Create_Cluster",
            variables=["KUBECONFIG"]
        )

    @action
    def GKE_Configure_CloudConsole():    
        CalmTask.Exec.ssh(
            filename="scripts/gke_configure_cloudconsole.sh",
            name="GKE_Configure_CloudConsole"
        )

    @action
    def Centos_Install_Docker():
        CalmTask.Exec.ssh(
            filename="scripts/centos_install_docker.sh",
            name="Install_Docker"
        )

    @action
    def NTNXPC_Extend_Disk():
        CalmTask.Exec.escript(
            filename="scripts/ntnxpc_extend_disk.py",
            name="Extend_OS_Disk"
        )

    @action
    def NTNXK8S_Install_CSI():
        CalmTask.Exec.ssh(
            filename="scripts/ntnxk8s_install_csi.sh",
            name="NTNXK8S_Install_CSI"
        )

    GCP_PROJECT_ID = Variable.Simple.string(
        "",
        name="GCP_PROJECT_ID"
    )

    GCP_KEY = Variable.Simple.string(
        "",
        name="GCP_KEY",
        is_hidden=True
    )

    KUBECONFIG = Variable.Simple.string(
        "",
        name="KUBECONFIG"
    )


class AdminVM_Package(Package):

    services = [ref(AdminVM)]

    @action
    def __install__():
        AdminVM.NTNXPC_Extend_Disk(name="NTNXPC_Extend_Disk")
        AdminVM.Centos_Install_Docker(name="Centos_Install_Docker")
        AdminVM.Gcloud_Install_SDK(name="Gcloud_Install_SDK")
        AdminVM.Anthos_Install_CLI(name="Anthos_Install_CLI")


class AdminVM_Substrate(Substrate):

    os_type = "Linux"
    
    provider_spec = read_ahv_spec(
        "specs/substrate/adminVm-spec.yaml",
        disk_packages={1: AHV_CENTOS}
    )
    provider_spec.spec["name"] = "@@{ANTHOS_CLUSTER_NAME}@@-anthos-adminVm-@@{calm_array_index}@@"

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(CRED_OS),
    }


class AdminVM_Deployment(Deployment):

    min_replicas = "1"
    max_replicas = "1"

    packages = [ref(AdminVM_Package)]
    substrate = ref(AdminVM_Substrate)


class Default(Profile):

    deployments = [
        AdminVM_Deployment,
        ControlPlaneVMs_Deployment,
        WorkerNodesVMs_Deployment
    ]

    ANTHOS_CLUSTER_NAME = Variable.Simple.string(
        "",
        name="ANTHOS_CLUSTER_NAME",
        label="Anthos cluster name",
        is_mandatory=True,
        runtime=True
    )

    ANTHOS_CONTROLPLANE_VIP = Variable.Simple.string(
        "192.168.4.2",
        name="ANTHOS_CONTROLPLANE_VIP",
        label="Anthos cluster VIP",
        description="This is the IP address for Kubernetes API. Format: XXX.XXX.XXX.XXX",
        is_mandatory=True,
        runtime=True
    )

    ANTHOS_PODS_NETWORK = Variable.Simple.string(
        "172.30.0.0/16",
        name="ANTHOS_PODS_NETWORK",
        label="Anthos Kubernetes pods network",
        description="""This is the network for your pods. Preferably do not overlap with other networks. 
            CIDR format: XXX.XXX.XXX.XXX/XX""",
        is_mandatory=True,
        runtime=True
    )

    ANTHOS_SERVICES_NETWORK = Variable.Simple.string(
        "172.31.0.0/16",
        name="ANTHOS_SERVICES_NETWORK",
        label="Anthos Kubernetes services network",
        description="""This is the network for your services. Preferably do not overlap with other networks. 
            CIDR format: XXX.XXX.XXX.XXX/XX""",
        is_mandatory=True,
        runtime=True
    )

    ANTHOS_INGRESS_VIP = Variable.Simple.string(
        "192.168.4.3",
        name="ANTHOS_INGRESS_VIP",
        label="Anthos Kubernetes Ingress VIP",
        description="""This is the IP address for Kubernetes Ingress. 
            This address MUST be within the load balancing pool. Format: XXX.XXX.XXX.XXX""",
        is_mandatory=True,
        runtime=True
    )

    ANTHOS_LB_ADDRESSPOOL = Variable.Simple.string(
        "192.168.4.3-192.168.4.5",
        name="ANTHOS_LB_ADDRESSPOOL",
        label="Anthos Load Balancing pool",
        description="""This is the IP address range for Load Balancing. 
            Format: XXX.XXX.XXX.XXX-YYY.YYY.YYY.YYY""",
        is_mandatory=True,
        runtime=True
    )

    KUBERNETES_SERVICE_ACCOUNT = Variable.Simple.string(
        "google-cloud-console",
        name="KUBERNETES_SERVICE_ACCOUNT",
        label="Kubernetes SA Cloud Console",
        description="""
            This K8s SA is for Google Cloud Console so the K8s cluster can be managed in GKE. 
            This service account will have cluster-admin role for Google Cloud Marketplace to work. 
            Default: google-cloud-console""",
        is_mandatory=True,
        runtime=True
    )

    OS_DISK_SIZE = Variable.Simple.int(
        "128",
        name="OS_DISK_SIZE",
        label="OS disk size",
        is_hidden=True
    )

    PYTHON_ANTHOS_GENCONFIG = Variable.Simple.string(
        "https://raw.githubusercontent.com/pipoe2h/calm-dsl/anthos-on-ahv/blueprints/anthos-on-ahv/scripts/anthos_generate_config.py",
        name="PYTHON_ANTHOS_GENCONFIG",
        label="Python Parser URL",
        description="""This script is hosted externally and produce an Anthos configuration 
            file for cluster creation with user provided inputs during launch""",
        is_hidden=True
    )

    NTNX_CSI_URL = Variable.Simple.string(
        "http://download.nutanix.com/csi/v2.3.1/csi-v2.3.1.tar.gz",
        name="NTNX_CSI_URL",
        label="Nutanix CSI Driver URL",
        is_hidden=True
    )

    NTNX_PE_IP = Variable.Simple.string(
        "192.168.2.40",
        name="NTNX_PE_IP",
        label="Prism Element VIP",
        description="This is needed for the CSI driver to create persistent volumes via the API",
        is_hidden=True
    )

    NTNX_PE_PORT = Variable.Simple.string(
        "9440",
        name="NTNX_PE_PORT",
        label="Prism Element port",
        is_hidden=True
    )

    NTNX_PE_DATASERVICE_IP = Variable.Simple.string(
        "192.168.2.41",
        name="NTNX_PE_DATASERVICE_IP",
        label="Data service IP address",
        description="""Data service is required to allow iSCSI connectivity between the 
            Kubernetes pods and the volumes created by CSI""",
        is_hidden=True
    )

    NTNX_PE_STORAGE_CONTAINER = Variable.Simple.string(
        "SelfServiceContainer",
        name="NTNX_PE_STORAGE_CONTAINER",
        label="Storage Container in Prism Element",
        description="""This is the Nutanix Storage Container where the requested Persistent Volume Claims will
            get their volumes created. You can enable things like compression and deduplication in a Storage Container""",
        is_hidden=True
    )

class Anthos_on_AHV(Blueprint):

    credentials = [
        CRED_OS,
        CRED_PE,
        CRED_GCLOUD
    ]
    services = [
        AdminVM,
        ControlPlaneVMs,
        WorkerNodesVMs
    ]
    packages = [
        AdminVM_Package,
        ControlPlaneVMs_Package,
        WorkerNodesVMs_Package,
        AHV_CENTOS
    ]
    substrates = [
        AdminVM_Substrate,
        ControlPlaneVMs_Substrate,
        WorkerNodesVMs_Substrate
    ]
    profiles = [Default]

def main():
    print(Anthos_on_AHV.json_dumps(pprint=True))


if __name__ == "__main__":
    main()