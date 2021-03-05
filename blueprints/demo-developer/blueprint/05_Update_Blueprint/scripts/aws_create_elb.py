AWS_ACCESS_KEY = '@@{CRED_AWS.username}@@'
AWS_SECRET_KEY = '@@{CRED_AWS.secret}@@'
AWS_REGION = '@@{AWS_REGION}@@'

from boto3 import client
from boto3 import setup_default_session

setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ec2_client = client('ec2')

# Get VPC ID
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

AWS_VPC = vpcs['Vpcs'][0]['VpcId']

# Get Subnet ID
subnets = ec2_client.describe_subnets(
    Filters=[
        {
            "Name": "default-for-az",
            "Values": [
                'true'
            ]
        }
    ]
)

print("AWS_VPC_CIDR={}".format(subnets['Subnets'][0]['CidrBlock']))


elb_client = client('elbv2')

# Create ELB
response = elb_client.create_load_balancer(
    Name='@@{calm_application_name}@@-elb',
    Subnets=[
        'subnet-4e314927',
        'subnet-6bff3427'
    ],
    SecurityGroups=[
        'sg-0022176bcc2307493',
    ],
    Scheme='internet-facing',
    Type='application',
    IpAddressType='ipv4'
)

elb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
elb_name = response['LoadBalancers'][0]['LoadBalancerName']
elb_dns = response['LoadBalancers'][0]['DNSName']

elb_complete_waiter = elb_client.get_waiter('load_balancer_available')

elb_complete_waiter.wait(LoadBalancerArns=[elb_arn])
print("Load balancer {} created".format(elb_name))
print("AWS_ELB_DNS={}".format(elb_dns))
print("AWS_ELB_ARN={}".format(elb_arn))

# Create ELB Target Group
response = elb_client.create_target_group(
    Name='@@{calm_application_name}@@-target',
    Protocol='HTTP',
    Port=80,
    VpcId=AWS_VPC,
    HealthCheckProtocol='HTTP',
    TargetType='ip',
)

elb_target_arn = response['TargetGroups'][0]['TargetGroupArn']
print("AWS_ELB_TARGET_ARN={}".format(elb_target_arn))

# Create ELB Listener
response = elb_client.create_listener(
    LoadBalancerArn=elb_arn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': elb_target_arn,
        },
    ]
)