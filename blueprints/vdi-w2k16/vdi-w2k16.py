import os

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint
from calm.dsl.builtins import CalmVariable as Variable
from calm.dsl.builtins import action, ref, basic_cred
from calm.dsl.builtins import read_local_file, read_provider_spec, read_file

# Windows Credentials
WINDOWS_USER = "Administrator"
WINDOWS_PASSWORD = read_local_file(
    os.path.join("secrets", "Windows_Local_Administrator_Password")
)
Windows_Local_Administrator = basic_cred(
    WINDOWS_USER, WINDOWS_PASSWORD, name="Windows_Local_Administrator", default=True,
)

# Domain Credentials
DOMAIN_USER = "UKDEMO\\jose.gomez"
DOMAIN_PASSWORD = read_local_file(os.path.join("secrets", "Domain_Join_User_Password"))
Domain_Join_User = basic_cred(
    DOMAIN_USER, DOMAIN_PASSWORD, name="Domain_Join_User", default=False,
)

# Windows License
WINDOWS_KEY = read_local_file(os.path.join("secrets", "Windows_License_Key"))


class VM(Service):
    @action
    def __create__():
        """Windows IaaS"""


class VM_AHV_Small_Package(Package):
    services = [ref(VM)]


class VM_AHV_Small_Substrate(Substrate):
    os_type = "Windows"
    provider_type = "AHV_VM"
    provider_spec = read_provider_spec("specs/vdi-spec.yaml")
    provider_spec.spec["resources"]["guest_customization"]["sysprep"][
        "unattend_xml"
    ] = read_file(os.path.join("scripts", "Autounattend.xml"))
    readiness_probe = {
        "credential": ref(Windows_Local_Administrator),
        "connection_type": "POWERSHELL",
        "connection_port": 5985,
        "delay_secs": "120",
        "retries": "20",
    }


class VM_AHV_Small_Deployment(Deployment):

    min_replicas = "1"
    max_replicas = "1"

    packages = [ref(VM_AHV_Small_Package)]
    substrate = ref(VM_AHV_Small_Substrate)


class AHV_Small(Profile):

    # Deployments under this profile
    deployments = [VM_AHV_Small_Deployment]

    # Profile Variables
    """Windows Server 2016 Standard - License key"""
    Windows_License_Key = Variable.Simple.Secret.string(WINDOWS_KEY, is_hidden=True)


class Windows_Server_Build(Blueprint):

    credentials = [Windows_Local_Administrator, Domain_Join_User]
    services = [VM]
    packages = [VM_AHV_Small_Package]
    substrates = [VM_AHV_Small_Substrate]
    profiles = [AHV_Small]
