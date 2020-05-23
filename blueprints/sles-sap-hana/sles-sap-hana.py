import os
import json

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint
from calm.dsl.builtins import action, ref, basic_cred, CalmTask
from calm.dsl.builtins import read_local_file, read_ahv_spec, read_vmw_spec, read_file
from calm.dsl.builtins import vm_disk_package
from calm.dsl.builtins import CalmVariable as Variable
from calm.dsl.builtins import read_env

# Import environment variables
ENV = read_env()

CENTOS_IMAGE_SOURCE = ENV.get("CENTOS_IMAGE_SOURCE")

# Credentials definition
OS_USERNAME = os.getenv("CALMDSL_OS_USERNAME") or read_local_file(
    os.path.join("secrets", "os_username")
)
OS_PASSWORD = os.getenv("CALMDSL_OS_PASSWORD") or read_local_file(
    os.path.join("secrets", "os_password")
)
Cred_OS = basic_cred(
    username=OS_USERNAME,
    password=OS_PASSWORD,
    name="Cred_OS",
    default=True,
    type="PASSWORD"
)

# ARTIFACTORY_USERNAME = "admin"
# ARTIFACTORY_PASSWORD = os.getenv("CALMDSL_ARTIFACTORY_PASSWORD") or read_local_file(
#     os.path.join("secrets", "artifactory_password")
# )
# Cred_ART = basic_cred(
#     username=ARTIFACTORY_USERNAME,
#     password=ARTIFACTORY_PASSWORD,
#     name="Cred_ART",
#     default=False,
#     type="PASSWORD"
# )

# Create Downloadable Disk
AHV_CENTOS_76 = vm_disk_package(
    name="AHV_CENTOS_76",
    config={
        "image": {
            "source": CENTOS_IMAGE_SOURCE
        }
    },
)


class ControlVM(Service):
    """Control Centre VM for managing SAP"""

    @action
    def Patch_Image():
        CalmTask.Exec.ssh(
            filename="scripts/shell/patch_image.sh",
            name="PatchImage"
        )

        IMG_URL = Variable.Simple.string('',name='IMG_URL')


class ControlVM_Package(Package):
    services = [ref(ControlVM)]

    @action
    def __install__():
        CalmTask.Exec.ssh(
            filename="scripts/shell/dependencies.sh",
            name="Dependencies"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/docker_install.sh",
            name="DockerInstall"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/docker_artifactory.sh",
            name="DockerArtifactoryInstall"
        )

        CalmTask.Delay(delay_seconds=90)

        CalmTask.Exec.escript(
            filename="scripts/escript/artifactory_initial_setup.py",
            name="ArtifactoryInitialSetup"
        )

class ControlVM_Substrate(Substrate):

    os_type = "Linux"
    
    provider_spec = read_ahv_spec(
        "specs/substrate/sapControlCentre-spec.yaml",
        disk_packages={1: AHV_CENTOS_76}
    )
    provider_spec.spec["name"] = "sap-control-centre-@@{calm_random}@@"
    
    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(Cred_OS),
    }


class ControlVM_Deployment(Deployment):

    min_replicas = "1"
    max_replicas = "1"

    packages = [ref(ControlVM_Package)]
    substrate = ref(ControlVM_Substrate)


class Default(Profile):

    deployments = [
        ControlVM_Deployment
    ]

    ARTIFACTORY_PASSWORD = Variable.Simple.Secret.string(
        'nutanix/4u',
        name="ARTIFACTORY_PASSWORD",
        label="Password for Image Repository",
        is_mandatory=True,
        runtime=True
    )

    @action
    def Patch_Image():
        
        ControlVM.Patch_Image(
            name="PatchImage"
        )

        # ControlVmIp = Variable.Simple.string(
        #     '',
        #     name="ControlVmIp",
        #     label='Control VM IP address',
        #     is_mandatory=True,
        #     runtime=True
        # )

        # IMG_TEST = Variable.WithOptions.FromTask(
        #     CalmTask.HTTP.get(
        #         "http://@@{ControlVmIP}@@:8082/artifactory/api/storage/official-isos/",
        #         # Headers in HTTP variables are bugged:
        #         # https://jira.nutanix.com/browse/CALM-13724
        #         # headers={"Content-Type": "application/json"},
        #         content_type="application/json",
        #         verify=False,
        #         status_mapping={200: True},
        #         name="IMG_URI",
        #         response_paths={"IMG_URI": "$.children[*].uri"}
        #     ),
        #     label="Select Official ISO",
        #     is_mandatory=True
        # )        

        # IMG_URI = Variable.WithOptions.FromTask(
        #     CalmTask.Exec.escript(
        #         filename="scripts/escript/list_official_images.py",
        #         name="IMG_URI"
        #     ),
        #     label="Official ISOs",
        #     is_mandatory=True
        # )

        IMG_URL = Variable.Simple.string(
            '',
            name="IMG_URL",
            label="Provide the ISO link",
            is_mandatory=True,
            runtime=True
        )


class Sap_Control_Centre(Blueprint):
    """* [Repo](http://@@{ControlVM.address}@@:8082/ui)"""

    credentials = [
        Cred_OS,
        # Cred_ART
    ]
    services = [
        ControlVM
    ]
    packages = [
        ControlVM_Package,
        AHV_CENTOS_76
    ]
    substrates = [
        ControlVM_Substrate
    ]
    profiles = [Default]


def main():
    print(Sap_Control_Centre.json_dumps(pprint=True))


if __name__ == "__main__":
    main()