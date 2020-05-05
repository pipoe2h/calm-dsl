AWS_ACCESS_KEY = '@@{Cred_AWS.username}@@'
AWS_SECRET_KEY = '@@{Cred_AWS.secret}@@'
AWS_REGION = '@@{AWS_REGION}@@'

from boto3 import client
from boto3 import setup_default_session
import json

setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ec2_client = client('ec2')

vpcs = ec2_client.describe_vpcs(
    Filters=[
        {
            "Name": "isDefault",
            "Values": [
                'true'
            ]
        }
    ]
)

AWS_VCP = vpcs['Vpcs'][0]['VpcId']
print("AWS_VCP={}".format(AWS_VCP))

security_groups = ec2_client.describe_security_groups()

if "NTNX_MOVE_DEMO_CENTOS" not in json.dumps(security_groups):

    response = ec2_client.create_security_group(
        Description='Nutanix Move Demo - Allow HTTP and SSH',
        GroupName='NTNX_MOVE_DEMO_CENTOS',
        VpcId=AWS_VCP
    )

    sg_id = response['GroupId']

    response = ec2_client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'ToPort': 22,
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'SSH access from the Internet'
                    }
                ]
            },
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'ToPort': 80,
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'HTTP access from the Internet'
                    }
                ]
            }
        ]
    )

    print("AWS_SG_ID={}".format(sg_id))