"""
Move Blueprint

"""

from calm.dsl.builtins import ref, basic_cred
from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint, AhvVmResources, CalmVariable
from calm.dsl.builtins import read_ahv_spec, read_local_file
from calm.dsl.builtins import vm_disk_package, AhvVmNic, AhvVm, AhvVmDisk

import json


Cred_Move = basic_cred("username", "password", name="Cred_Move", default=True)

Move_Disk = vm_disk_package(
    name="move_disk",
    config={
        # By default image type is set to DISK_IMAGE
        "image": {
            "source": "@@{MOVE_IMAGE_URL}@@"
        }
    },
)


class MoveVM(Service):
    """Move service"""

    pass


class MovePackage(Package):
    """Move package"""

    services = [ref(MoveVM)]


class MoveVMS(Substrate):
    """Move Substrate"""

    provider_spec = read_ahv_spec(
        "specs/move_spec.yaml",
        disk_packages={1: Move_Disk}
    )

    provider_spec.spec['resources']['nic_list'].append(AhvVmNic("dnd-jose.gomez").compile())

    readiness_probe = {
        "disabled": True,
        "delay_secs": "0",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(Cred_Move),
    }


class MoveDeployment(Deployment):
    """Move Deployment"""

    packages = [ref(MovePackage)]
    substrate = ref(MoveVMS)


class AHV(Profile):
    """Move Profile"""

    deployments = [MoveDeployment]
    
    MOVE_IMAGE_URL = CalmVariable.Simple.string("", is_mandatory=True, runtime=True)


class MoveDslBlueprint(Blueprint):
    """* [Move for VMs](https://@@{MoveVM.address}@@)"""

    credentials = [Cred_Move]
    services = [MoveVM]
    packages = [MovePackage,Move_Disk]
    substrates = [MoveVMS]
    profiles = [AHV]


def main():
    print(MoveDslBlueprint.json_dumps(pprint=True))


if __name__ == "__main__":
    main()