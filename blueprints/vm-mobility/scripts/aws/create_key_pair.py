AWS_ACCESS_KEY = '@@{Cred_AWS.username}@@'
AWS_SECRET_KEY = '@@{Cred_AWS.secret}@@'
AWS_REGION = '@@{AWS_REGION}@@'

from boto3 import client
from boto3 import setup_default_session

setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ec2_client = client('ec2')

# Check if SSH Demo Key exists if not create
key_pairs = ec2_client.describe_key_pairs(KeyNames=['NTNX_MOVE_DEMO_CENTOS'])

if "NTNX_MOVE_DEMO_CENTOS" not in json.dumps(key_pairs):
    
    # Create SSH Key Pair
    response = ec2_client.create_key_pair(
        KeyName='NTNX_MOVE_DEMO_CENTOS'
    )
