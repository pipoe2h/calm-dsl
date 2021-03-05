from calm.dsl.builtins import Project
from calm.dsl.builtins import Provider, Ref


AHV_ACCOUNT = "NTNX_LOCAL_AZ"
AZ_ACCOUNT = "AZ_UK_PPS"
AWS_ACCOUNT = "AWS_UK_PPS"
K8S_ACCOUNT = "Anthos"
SUBNET = "dnd-demo"
CLUSTER = "Theale"
USER = "jose.gomez@ukdemo.local"
# GROUP = "cn=sspgroup1,ou=pc,dc=systest,dc=nutanix,dc=com"
VCPUS = 40
STORAGE = 1024  # GiB
MEMORY = 256  # GiB


class DevDslProject(Project):
    """Dev DSL Project"""

    providers = [
        Provider.Ntnx(
            account=Ref.Account(AHV_ACCOUNT),
            subnets=[Ref.Subnet(name=SUBNET, cluster=CLUSTER)],
        ),

        Provider.Azure(
            account=Ref.Account(AZ_ACCOUNT)
        ),

        Provider.Aws(
            account=Ref.Account(AWS_ACCOUNT)
        ),

        Provider.K8s(
            account=Ref.Account(K8S_ACCOUNT)
        )
    ]

    users = [Ref.User(name=USER)]

    # groups = [Ref.Group(name=GROUP)]

    # quotas = {"vcpus": VCPUS, "storage": STORAGE, "memory": MEMORY}