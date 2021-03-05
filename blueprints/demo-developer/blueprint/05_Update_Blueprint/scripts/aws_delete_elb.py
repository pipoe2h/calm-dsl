AWS_ACCESS_KEY = '@@{CRED_AWS.username}@@'
AWS_SECRET_KEY = '@@{CRED_AWS.secret}@@'
AWS_REGION = '@@{AWS_REGION}@@'
AWS_ELB_ARN = '@@{AWS_ELB_ARN}@@'
AWS_ELB_TARGET_ARN = '@@{AWS_ELB_TARGET_ARN}@@'

from boto3 import client
from boto3 import setup_default_session

setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

elb_client = client('elbv2')

# Delete ELB
response = elb_client.delete_load_balancer(
    LoadBalancerArn=AWS_ELB_ARN
)

elb_complete_waiter = elb_client.get_waiter('load_balancers_deleted')

elb_complete_waiter.wait(LoadBalancerArns=[AWS_ELB_ARN])
print("Load balancer {} deleted".format(AWS_ELB_ARN))

sleep(15)

# Delete ELB Target Group
response = elb_client.delete_target_group(
    TargetGroupArn=AWS_ELB_TARGET_ARN
)

print("Target group {} deleted".format(AWS_ELB_TARGET_ARN))
