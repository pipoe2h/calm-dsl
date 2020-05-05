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

PC_USERNAME = os.getenv("CALMDSL_PC_USERNAME") or read_local_file(
    os.path.join("secrets", "pc_username")
)
PC_PASSWORD = os.getenv("CALMDSL_PC_PASSWORD") or read_local_file(
    os.path.join("secrets", "pc_password")
)
Cred_PC = basic_cred(
    username=PC_USERNAME,
    password=PC_PASSWORD,
    name="Cred_PC",
    default=False,
    type="PASSWORD"
)

AWS_ACCESS_KEY = os.getenv("CALMDSL_AWS_ACCESS_KEY") or read_local_file(
    os.path.join("secrets", "aws_access_key")
)
AWS_SECRET_KEY = os.getenv("CALMDSL_AWS_SECRET_KEY") or read_local_file(
    os.path.join("secrets", "aws_secret_key")
)
Cred_AWS = basic_cred(
    username=AWS_ACCESS_KEY,
    password=AWS_SECRET_KEY,
    name="Cred_AWS",
    default=False,
    type="PASSWORD"
)

# Downloadable images for AHV and VMware
# AHV_CENTOS_76 = vm_disk_package(
#     name="AHV_CENTOS_76", config_file="specs/image_config/ahv_centos.yaml"
# )

AHV_CENTOS_76 = vm_disk_package(
    name="AHV_CENTOS_76",
    config={
        # By default image type is set to DISK_IMAGE
        "image": {
            "source": CENTOS_IMAGE_SOURCE
        }
    },
)


class ControlVM(Service):
    """Control VM for downloading Move """

    @action
    def DeployMove():
        CalmTask.Exec.ssh(
            filename="scripts/shell/move_deploy.sh",
            name="MoveDeployTask"
        )


class ControlVM_Package(Package):
    services = [ref(ControlVM)]

    @action
    def __install__():
        CalmTask.Exec.ssh(
            filename="scripts/shell/move_download.sh",
            name="PackageInstallTask"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/docker_install.sh",
            name="DockerInstallTask"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/dockerCompose_install.sh",
            name="DockerComposeInstallTask"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/dockerHttpd_run.sh",
            name="DockerHttpInstallTask"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/calmDsl_run.sh",
            name="CalmDslInstallTask"
        )


class ControlVM_Substrate(Substrate):
    os_type = "Linux"
    provider_spec = read_ahv_spec(
        "specs/substrate/controlVm-spec.yaml",
        disk_packages={1: AHV_CENTOS_76}
    )
    provider_spec.spec["name"] = "jg-moveControlVm-@@{calm_random}@@"
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

    Move_Version = Variable.Simple.string(
        "3.5.0",
        is_hidden=True
    )

    AWS_REGION = Variable.Simple.string(
        "eu-west-2",
        is_mandatory=True,
        runtime=True
    )

    PC_IP = Variable.Simple.string(
        "x.x.x.x",
        is_mandatory=True,
        runtime=True
    )

    PROJECT_NETWORK = Variable.WithOptions.FromTask(
        CalmTask.HTTP.post(
            "https://localhost:9440/api/nutanix/v3/projects/list",
            credential=Cred_PC,
            body=json.dumps({"filter": "name==@@{calm_project_name}@@"}),
            # Headers in HTTP variables are bugged:
            # https://jira.nutanix.com/browse/CALM-13724
            # headers={"Content-Type": "application/json"},
            content_type="application/json",
            verify=False,
            status_mapping={200: True},
            name="PROJECT_NETWORK",
            response_paths={"PROJECT_NETWORK": "$.entities[0].spec.resources.subnet_reference_list[*].name"}
        ),
        label="Select network"
    )

    @action
    def First_Deploy_Move():

        CalmTask.Exec.ssh(
            filename="scripts/shell/move_deploy.sh",
            name="MoveDeployTask",
            target=ref(ControlVM)
        )

    @action
    def Second_Deploy_AWS_Demo_VM():

        CalmTask.Exec.ssh(
            filename="scripts/shell/awsVm_deploy.sh",
            name="AwsVmDeployTask",
            target=ref(ControlVM)
        )
    
    @action
    def Third_Migrate_VM():
        """ccc"""

class Workload_Mobility_Setup(Blueprint):

    credentials = [
        Cred_OS,
        Cred_PC,
        Cred_AWS
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
    print(Workload_Mobility_Setup.json_dumps(pprint=True))


if __name__ == "__main__":
    main()