import os

from calm.dsl.builtins import action, ref, basic_cred, CalmTask
from calm.dsl.builtins import read_local_file, read_provider_spec

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint

from calm.dsl.builtins import CalmVariable as Variable

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

AWS_AMI_ID = os.getenv("CALMDSL_AWS_AMI_ID")
AWS_REGION = os.getenv("CALMDSL_AWS_REGION")
AWS_VPC_ID = os.getenv("CALMDSL_AWS_VPC_ID")
AWS_SG_ID = os.getenv("CALMDSL_AWS_SG_ID")
MOVE_VAPP_IP = os.getenv("CALMDSL_MOVE_VAPP_IP")
PE_UUID = os.getenv("CALMDSL_PE_UUID")
SC_UUID = os.getenv("CALMDSL_SC_UUID")
AHV_NETWORK = os.getenv("CALMDSL_AHV_NETWORK")
MOVE_AWS_PROVIDERUUID = os.getenv("CALMDSL_MOVE_AWS_PROVIDERUUID")
MOVE_AHV_PROVIDERUUID = os.getenv("CALMDSL_MOVE_AHV_PROVIDERUUID")

class AwsVmService(Service):
    """AWS VM"""

    MOVE_AWS_VM_UUID = Variable.Simple.string('',name='MOVE_AWS_VM_UUID')
    MOVE_AWS_VM_ID = Variable.Simple.string('',name='MOVE_AWS_VM_ID')

class AwsVmPackage(Package):

    services = [ref(AwsVmService)]

    @action
    def __install__():
        CalmTask.Exec.ssh(
            filename="scripts/centos_install_httpd.sh",
            name="PackageInstallTask"
        )


class AwsVmSubstrate(Substrate):
    """AWS VM config given by reading a spec file"""

    provider_spec = read_provider_spec("specs/aws_spec_centos.yaml")
    provider_spec.spec['resources']['image_id'] = AWS_AMI_ID
    provider_spec.spec['resources']['region'] = AWS_REGION
    provider_spec.spec['resources']['vpc_id'] = AWS_VPC_ID
    provider_spec.spec['resources']['security_group_list'] = [
        {"security_group_id": AWS_SG_ID}
    ]
    provider_type = "AWS_VM"
    os_type = "Linux"
    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(Cred_OS),
    }


class AwsVmDeployment(Deployment):
    """Sample deployment pulling in service and substrate references"""

    packages = [ref(AwsVmPackage)]
    substrate = ref(AwsVmSubstrate)


class AwsVmProfile(Profile):
    """Sample application profile with variables"""

    deployments = [AwsVmDeployment]

    Move_IP = Variable.Simple.string(
        MOVE_VAPP_IP,
        is_hidden=True
    )

    peUuid = Variable.Simple.string(
        PE_UUID,
        is_hidden=True
    )

    scUuid = Variable.Simple.string(
        SC_UUID,
        is_hidden=True
    )

    awsVpcId = Variable.Simple.string(
        AWS_VPC_ID,
        is_hidden=True
    )

    ahvNetwork = Variable.Simple.string(
        AHV_NETWORK,
        is_hidden=True
    )

    awsRegion = Variable.Simple.string(
        AWS_REGION,
        is_hidden=True
    )

    moveAwsProviderUuid = Variable.Simple.string(
        MOVE_AWS_PROVIDERUUID,
        is_hidden=True
    )

    moveAhvProviderUuid = Variable.Simple.string(
        MOVE_AHV_PROVIDERUUID,
        is_hidden=True
    )

    @action
    def MigrateWorkload():

        CalmTask.SetVariable.escript(
            filename="scripts/get_ec2.py",
            name="GetEc2Task",
            variables=['MOVE_AWS_VM_UUID','MOVE_AWS_VM_ID'],
            target=ref(AwsVmService)
        )

        CalmTask.Exec.escript(
            filename="scripts/move_create_migration_plan.py",
            name="CreateMigrationPlanTask",
            target=ref(AwsVmService)
        )


class AwsBlueprint(Blueprint):
    """* [WebApp](http://@@{AwsVmService.address}@@)"""

    credentials = [Cred_OS]
    services = [AwsVmService]
    packages = [AwsVmPackage]
    substrates = [AwsVmSubstrate]
    profiles = [AwsVmProfile]


def test_json():
    print(AwsBlueprint.json_dumps(pprint=True))


if __name__ == "__main__":
    test_json()