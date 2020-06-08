import os
import json

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint
from calm.dsl.builtins import ref, basic_cred, action, CalmTask
from calm.dsl.builtins import CalmVariable as Variable
from calm.dsl.builtins import read_ahv_spec, read_local_file
from calm.dsl.builtins import vm_disk_package


# Credentials definition
try:
    OS_USERNAME = os.getenv("CALMDSL_OS_USERNAME") or read_local_file(
        os.path.join("secrets", "os_username")
    )
except FileNotFoundError:
    OS_USERNAME = "ubuntu"

try:  
    OS_PASSWORD = os.getenv("CALMDSL_OS_PASSWORD") or read_local_file(
        os.path.join("secrets", "os_password")
    )
except FileNotFoundError:
    OS_PASSWORD = "nutanix/4u"

Cred_OS = basic_cred(
    username=OS_USERNAME,
    password=OS_PASSWORD,
    name="Cred_OS",
    default=True,
    type="PASSWORD"
)


class dev_station(Service):
    """Developer Station Service"""

    DEVELOPER_USERNAME = Variable.Simple.string(
        '',
        name="DEVELOPER_USERNAME",
        is_hidden=True
    )


class dev_station_package(Package):
    """Developer Station Package"""

    services = [ref(dev_station)]

    @action
    def __install__():

        CalmTask.Exec.escript(
            filename="scripts/escript/expand_disk.py",
            name="ExpandDisk"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/base_system.sh",
            name="BaseSystem"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/docker_install.sh",
            name="DockerInstall"
        )

        CalmTask.Exec.ssh(
            filename="scripts/shell/dockerCompose_install.sh",
            name="DockerComposeInstall"
        )


AHV_UBUNTU_20_04 = vm_disk_package(
    name="AHV_UBUNTU_20_04", 
    config_file="specs/image_config/ahv_ubuntu.yaml"
)


class dev_station_substrate(Substrate):
    """Developer Station Substrate"""

    os_type = "Linux"

    provider_spec = read_ahv_spec(
        "specs/substrate/dev_station_spec.yaml",
        disk_packages={1: AHV_UBUNTU_20_04}
    )
    provider_spec.spec["name"] = "devStation-@@{calm_random}@@"

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(Cred_OS),
    }

    @action
    def __pre_create__():
        CalmTask.SetVariable.escript(
            "print('DEVELOPER_USERNAME={}'.format('@@{calm_username}@@'.split('@')[0]))",
            name="GetUsername",
            variables=["DEVELOPER_USERNAME"]
        )

class dev_station_deployment(Deployment):
    """Developer Station Deployment"""

    min_replicas = "1"
    max_replicas = "1"

    packages = [ref(dev_station_package)]
    substrate = ref(dev_station_substrate)


class Default(Profile):
    """Developer Station Profile"""

    deployments = [dev_station_deployment]

    # DEVELOPER_USERNAME = Variable.Simple.string(
    #     # "name.surname",
    #     "jose.gomez",
    #     name="DEVELOPER_USERNAME",
    #     label="Your username",
    #     is_mandatory=True,
    #     runtime=True
    # )

    DEVELOPER_PUB_KEY = Variable.Simple.string(
        # "ssh-rsa ...",
        "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAlfStbqnKNNpjH6LBFcbyIbGTkougx9GDfvzUEseWJWdn9oomF0y/w7yymB+ulzs5Ftx32mWNGAR/yTGI+OKzVin9B1kmUsHXGmwdGKgSiF26v3ejHOHbLXpRLpm9UwpusxUzwJfnlCFipwjLxTol4ARLliTnvidq1G/hGttZ5GPozukkuZJLQ0M5I4B0BSqO3mzUmhjlOb5BPSfUUM51loMZ01RzqJAF361/SPvwQhv0WIB00P10iqlo0Rsost392AW4L4x3vPgdtBIurEV81Ox0M/N4qBIdtdwh3KSwu4DtqZyAr9PlDnW+w51r53TT1AkHiGJJP03dTjA9aGh4gw==",
        name="DEVELOPER_PUB_KEY",
        label="Your SSH public key",
        is_mandatory=True,
        runtime=True
    )

    ROOT_DISK_SIZE = Variable.Simple.int(
        '8',
        label="New OS root partition size",
        is_hidden=True
    )

    DOCKER_REGISTRIES_CIDR = Variable.Simple.string(
        '192.168.0.0/16',
        label="Network CIDR hosting insecure registries (self-signed)",
        is_hidden=True
    )


class Developer_Station(Blueprint):
    """Developer Station"""

    credentials = [Cred_OS]
    services = [dev_station]
    packages = [
        dev_station_package,
        AHV_UBUNTU_20_04
    ]
    substrates = [dev_station_substrate]
    profiles = [Default]


def main():
    print(Developer_Station.json_dumps(pprint=True))


if __name__ == "__main__":
    main()

