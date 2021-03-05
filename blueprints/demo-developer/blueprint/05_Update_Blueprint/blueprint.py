import json
import os

from calm.dsl.builtins import ref, basic_cred
from calm.dsl.builtins import action, parallel
from calm.dsl.builtins import CalmTask, CalmVariable
from calm.dsl.builtins import AhvVm, AhvVmResources, AhvVmDisk, AhvVmNic, AhvVmGC
from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint, PODDeployment
from calm.dsl.builtins import read_local_file, read_provider_spec, provider_spec, read_spec

# Secret Variables
BP_CRED_Administrator_KEY = read_local_file("BP_CRED_Administrator_KEY")
BP_CRED_AWS_KEY_ID = read_local_file("BP_CRED_AWS_KEY_ID")
BP_CRED_AWS_SECRET_ID = read_local_file("BP_CRED_AWS_SECRET_ID")
BP_CRED_Docker_Username = read_local_file("BP_CRED_Docker_Username")
BP_CRED_Docker_Password = read_local_file("BP_CRED_Docker_Password")
BP_CRED_K8s_SA = read_local_file("BP_CRED_K8s_SA")
BP_CRED_K8s_Token = read_local_file("BP_CRED_K8s_Token")

# Credentials
BP_CRED_Administrator = basic_cred(
    "centos",
    BP_CRED_Administrator_KEY,
    name="CRED_CENTOS",
    type="KEY",
    default=True,
)

BP_CRED_AWS = basic_cred(
    BP_CRED_AWS_KEY_ID,
    filename=".local/BP_CRED_AWS_SECRET_ID",
    name="CRED_AWS",
    type="PASSWORD"
)

BP_CRED_Docker = basic_cred(
    BP_CRED_Docker_Username,
    BP_CRED_Docker_Password,
    name="CRED_DOCKER",
    type="PASSWORD"
)

BP_CRED_K8S = basic_cred(
    BP_CRED_K8s_SA,
    BP_CRED_K8s_Token,
    name="CRED_K8S",
    type="KEY"
)


class ApacheAHV(Service):

    @action
    def InstallDocker():
        CalmTask.Exec.ssh(
            name="Install Docker",
            filename="scripts/centos_install_docker.sh"
        )
    
    @action
    def InstallWebApp():
        PLATFORM = CalmVariable.Simple.string(
            "nutanix",
            name="PLATFORM",
            is_hidden=True
        )

        CalmTask.Exec.ssh(
            name="Install WebApp",
            filename="scripts/dockerHttpd_run.sh"
        )

class ApacheAHVPackage(Package):

    services = [ref(ApacheAHV)]

    @action
    def __install__():
        ApacheAHV.InstallDocker(name="InstallDocker")
        ApacheAHV.InstallWebApp(name="InstallWebApp")


class ApacheAhvVmResources(AhvVmResources):

    memory = 8
    vCPUs = 2
    cores_per_vCPU = 2
    disks = [
        AhvVmDisk.Disk.Scsi.cloneFromImageService("CENTOS_77", bootable=True)
    ]
    nics = [AhvVmNic.NormalNic.ingress("dnd-demo", cluster="Theale")]

    guest_customization = AhvVmGC.CloudInit(filename="specs/guest_custom.yaml")


class ApacheAhvVm(AhvVm):

    name = "@@{calm_application_name}@@-ahv-web-@@{calm_array_index}@@"
    resources = ApacheAhvVmResources


class ApacheAhvSubstrate(Substrate):
    
    provider_spec = ApacheAhvVm

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "retries": "5",
        "connection_type": "SSH",
        "connection_port": 22,
        "credential": ref(BP_CRED_Administrator),
    }


class ApacheAhvDeployment(Deployment):
    
    min_replicas = "1"
    max_replicas = "3"
    default_replicas = "1"

    packages = [ref(ApacheAHVPackage)]
    substrate = ref(ApacheAhvSubstrate)


class ApacheAWS(Service):

    @action
    def InstallDocker():
        CalmTask.Exec.ssh(
            name="Install Docker",
            filename="scripts/centos_install_docker.sh"
        )
    
    @action
    def InstallWebApp():
        PLATFORM = CalmVariable.Simple.string(
            "aws",
            name="PLATFORM",
            is_hidden=True
        )

        CalmTask.Exec.ssh(
            name="Install WebApp",
            filename="scripts/dockerHttpd_run.sh"
        )


class ApacheAWSPackage(Package):

    services = [ref(ApacheAWS)]

    @action
    def __install__():
        ApacheAWS.InstallDocker(name="InstallDocker")
        ApacheAWS.InstallWebApp(name="InstallWebApp")


class ApacheAwsSubstrate(Substrate):
    
    provider_type = "AWS_VM"
    provider_spec = read_provider_spec(filename="specs/aws_apache_spec.yaml")

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "retries": "5",
        "connection_type": "SSH",
        "connection_port": 22,
        "address": "@@{private_ip_address}@@",
        "credential": ref(BP_CRED_Administrator),
    }


class ApacheAwsDeployment(Deployment):
    
    min_replicas = "1"
    max_replicas = "3"
    default_replicas = "1"

    packages = [ref(ApacheAWSPackage)]
    substrate = ref(ApacheAwsSubstrate)


class ApacheAZ(Service):

    @action
    def __create__():
        ApacheAZ.AzureCreateElbTargets(name="AzureCreateElbTargets")

    @action
    def InstallDocker():
        CalmTask.Exec.ssh(
            name="Install Docker",
            filename="scripts/centos_install_docker.sh"
        )
    
    @action
    def InstallWebApp():
        PLATFORM = CalmVariable.Simple.string(
            "azure",
            name="PLATFORM",
            is_hidden=True
        )

        CalmTask.Exec.ssh(
            name="Install WebApp",
            filename="scripts/dockerHttpd_run.sh"
        )

    @action
    def AzureCreateElbTargets():
        CalmTask.Exec.escript(
            name="Create ELB Targets Azure",
            filename="scripts/aws_register_elb_targets_azure.py"
        )


class ApacheAZPackage(Package):

    services = [ref(ApacheAZ)]

    @action
    def __install__():
        ApacheAZ.InstallDocker(name="InstallDocker")
        ApacheAZ.InstallWebApp(name="InstallWebApp")

class ApacheAzureSubstrate(Substrate):
    
    provider_type = "AZURE_VM"
    provider_spec = read_provider_spec(filename="specs/azure_apache_spec.yaml")

    readiness_probe = {
        "disabled": False,
        "delay_secs": "60",
        "retries": "5",
        "connection_type": "SSH",
        "connection_port": 22,
        "address": "@@{platform.privateIPAddressList[0]}@@",
        "credential": ref(BP_CRED_Administrator),
    }


class ApacheAzureDeployment(Deployment):
    
    min_replicas = "1"
    max_replicas = "3"
    default_replicas = "1"

    packages = [ref(ApacheAZPackage)]
    substrate = ref(ApacheAzureSubstrate)


class ApacheK8s(Service):

    PLATFORM = CalmVariable.Simple.string(
        "k8s",
        name="PLATFORM",
        is_hidden=True
    )

    @action
    def K8sSetImage():
        CalmTask.Exec.escript(
            filename="scripts/k8s_set_image.py",
            name="K8sSetImage"
        )


class ApacheK8sDeployment(PODDeployment):
    """ Hybrid WebApp Deployment on K8S """

    containers = [ApacheK8s]
    deployment_spec = read_spec("specs/k8s_deployment.yaml")
    service_spec = read_spec("specs/k8s_service.yaml")


class AwsELB(Service):

    @action
    def __create__():
        AwsELB.AwsCreateElbTargets(name="AwsCreateElbTargets")

    @action
    def __delete__():
        AwsELB.AwsDeleteElb(name="AwsDeleteElb")


    @action
    def AwsCreateElbTargets():
        CalmTask.SetVariable.escript(
            name="Create ELB Targets",
            filename="scripts/aws_register_elb_targets.py",
            variables=["WEB_SERVERS"]
        )

    @action
    def AwsDeleteElbTargets():
        CalmTask.SetVariable.escript(
            name="Deregister ELB Targets",
            filename="scripts/aws_deregister_elb_targets.py",
            variables=["WEB_SERVERS"]
        )

    @action
    def AwsDeleteElb():
        CalmTask.Exec.escript(
            name="Delete ELB Load Balancer and Targets",
            filename="scripts/aws_delete_elb.py"
        )

    WEB_SERVERS = CalmVariable.Simple.string(
        "",
        name="WEB_SERVERS"
    )

class AwsELBPackage(Package):

    services = [ref(AwsELB)]


class AwsELBSubstrate(Substrate):
    """AWS Elastic Load Balancer"""

    provider_type = "EXISTING_VM"
    provider_spec = provider_spec({"address": "localhost"})
    readiness_probe = {
        "disabled": True,
        "delay_secs": "0",
        "connection_type": "SSH",
        "connection_port": 22
    }

    @action
    def __pre_create__():
        CalmTask.SetVariable.escript(
            name="Create ELB", 
            filename="scripts/aws_create_elb.py",
            variables=["AWS_ELB_ARN","AWS_ELB_DNS","AWS_ELB_TARGET_ARN","AWS_VPC_CIDR"]
        )


class AwsELBDeployment(Deployment):
    
    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(AwsELBPackage)]
    substrate = ref(AwsELBSubstrate)


class Hybrid(Profile):

    deployments = [ApacheAhvDeployment, 
        ApacheAwsDeployment, 
        ApacheAzureDeployment, 
        AwsELBDeployment,
        ApacheK8sDeployment
    ]

    AWS_REGION = CalmVariable.Simple.string(
       "eu-west-2",
       name="AWS_REGION" 
    )

    KUBERNETES_CLUSTER_IP = CalmVariable.Simple.string(
        "",
        name="KUBERNETES_CLUSTER_IP",
        is_mandatory=True,
        runtime=True
    )

    KUBERNETES_CLUSTER_PORT = CalmVariable.Simple.string(
        "443",
        name="KUBERNETES_CLUSTER_IP",
        is_mandatory=True,
        runtime=True
    )

    KUBERNETES_CLUSTER_VERIFY_SSL = CalmVariable.WithOptions.Predefined.string(
        ["False","True"],
        "False",
        name="KUBERNETES_CLUSTER_VERIFY_SSL",
        is_mandatory=True,
        runtime=True
    )

    KUBERNETES_NAMESPACE_NAME = CalmVariable.Simple.string(
        "default",
        name="KUBERNETES_NAMESPACE_NAME",
        is_mandatory=True,
        runtime=True
    )

    KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE = CalmVariable.Simple.string(
        "ukdemo/webpage:latest",
        name="KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE",
        is_mandatory=True,
        runtime=True
    )

    @action
    def ScaleOut():
        """This action will scale out by given scale out count"""
        Scaleout = CalmVariable.Simple.int(
            "1", 
            is_mandatory=True, 
            runtime=True
        )


        with parallel():
            CalmTask.Scaling.scale_out(
                "@@{Scaleout}@@",
                target=ref(ApacheAhvDeployment),
                name="Scale out AHV"
            )
            CalmTask.Scaling.scale_out(
                "@@{Scaleout}@@",
                target=ref(ApacheAwsDeployment),
                name="Scale out AWS"
            )
            CalmTask.Scaling.scale_out(
                "@@{Scaleout}@@",
                target=ref(ApacheAzureDeployment),
                name="Scale out Azure"
            )
            CalmTask.Scaling.scale_out(
                "@@{Scaleout}@@",
                target=ref(ApacheK8sDeployment),
                name="Scale out K8s"
            )


        # CalmTask.SetVariable.escript(
        #     name="Register ELB Targets",
        #     filename="scripts/aws_register_elb_targets.py",
        #     target=ref(AwsELB),
        #     variables=["WEB_SERVERS"]
        # )

        AwsELB.AwsCreateElbTargets(name="AwsCreateElbTargets")
        ApacheAZ.AzureCreateElbTargets(name="AzureCreateElbTargets")

    @action
    def ScaleIn():
        """This action will scale in by given scale in count"""
        ScaleIn = CalmVariable.Simple.int(
            "1", 
            is_mandatory=True, 
            runtime=True
        )
        
        with parallel():
            CalmTask.Scaling.scale_in(
                "@@{ScaleIn}@@", 
                target=ref(ApacheAhvDeployment), 
                name="Scale in AHV"
            )
            CalmTask.Scaling.scale_in(
                "@@{ScaleIn}@@", 
                target=ref(ApacheAwsDeployment), 
                name="Scale in AWS"
            )
            CalmTask.Scaling.scale_in(
                "@@{ScaleIn}@@", 
                target=ref(ApacheAzureDeployment), 
                name="Scale in Azure"
            )
            CalmTask.Scaling.scale_in(
                "@@{ScaleIn}@@", 
                target=ref(ApacheK8sDeployment), 
                name="Scale in K8s"
            )

        AwsELB.AwsDeleteElbTargets(name="AwsDeleteElbTargets")


    @action
    def UpdateApp():
        """This action will update the application with a new container image version"""

        KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE = CalmVariable.Simple.string(
            "",
            name="KUBERNETES_DEPLOYMENT_CONTAINER_IMAGE",
            is_mandatory=True,
            runtime=True
        )

        with parallel():
            ApacheK8s.K8sSetImage(name="K8sSetImage")
            ApacheAHV.InstallWebApp(name="InstallWebAppAHV")
            ApacheAWS.InstallWebApp(name="InstallWebAppAWS")
            ApacheAZ.InstallWebApp(name="InstallWebAppAZ")

class devdsl(Blueprint):
    """*[WebApp](http://@@{AwsELB.AWS_ELB_DNS}@@)"""

    services = [ApacheAHV,ApacheAWS,ApacheAZ,ApacheK8s,AwsELB]
    substrates = [ApacheAhvSubstrate,ApacheAwsSubstrate,ApacheAzureSubstrate,AwsELBSubstrate]
    packages = [ApacheAHVPackage,ApacheAWSPackage,ApacheAZPackage,AwsELBPackage]
    profiles = [Hybrid]
    credentials = [BP_CRED_Administrator,BP_CRED_AWS,BP_CRED_Docker,BP_CRED_K8S]


def test_json():
    print(devdsl.json_dumps(pprint=True))


if __name__ == "__main__":
    test_json()
