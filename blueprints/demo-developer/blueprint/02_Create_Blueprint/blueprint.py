import json
import os

from calm.dsl.builtins import *

# Secret Variables
BP_CRED_Administrator_KEY = read_local_file("BP_CRED_Administrator_KEY")

# Credentials
BP_CRED_Administrator = basic_cred(
    "centos",
    BP_CRED_Administrator_KEY,
    name="CRED_CENTOS",
    type="KEY",
    default=True,
)


class CentOSService(Service):

    pass


class CentOSPackage(Package):

    services = [ref(CentOSService)]


class CentOSAhvVmResources(AhvVmResources):

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk.Disk.Scsi.cloneFromImageService("CENTOS_77", bootable=True)
    ]
    nics = [AhvVmNic.NormalNic.ingress("dnd-demo", cluster="Theale")]

    guest_customization = AhvVmGC.CloudInit(filename="specs/guest_custom.yaml")


class CentOSAhvVm(AhvVm):

    name = "@@{calm_application_name}@@"
    resources = CentOSAhvVmResources


class CentOSAhvSubstrate(Substrate):
    
    provider_spec = CentOSAhvVm


class CentOSDeploymentBUG(Deployment):
    
    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(CentOSPackage)]
    substrate = ref(CentOSAhvSubstrate)


class AHV(Profile):

    deployments = [CentOSDeploymentBUG]


class jgdevdsl(Blueprint):

    services = [CentOSService]
    substrates = [CentOSAhvSubstrate]
    packages = [CentOSPackage]
    profiles = [AHV]
    credentials = [BP_CRED_Administrator]


def test_json():
    print(devdsl.json_dumps(pprint=True))


if __name__ == "__main__":
    test_json()
