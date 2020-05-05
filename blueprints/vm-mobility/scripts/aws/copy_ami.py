AWS_ACCESS_KEY = '@@{Cred_AWS.username}@@'
AWS_SECRET_KEY = '@@{Cred_AWS.secret}@@'
AWS_REGION = '@@{AWS_REGION}@@'
AWS_SOURCE_AMI = '@@{AWS_SOURCE_AMI}@@'

from boto3 import client
from boto3 import setup_default_session

setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ec2_client = client('ec2')
images = ec2_client.describe_images(
    Owners=['self'],
    Filters=[
        {
            "Name": "name",
            "Values": [
                'Nutanix Move CentOS Demo'
            ]
        }        
    ]
)

if "Nutanix Move CentOS Demo" not in json.dumps(images):

    response = ec2_client.copy_image(
        Name = "Nutanix Move CentOS Demo",
        SourceImageId = AWS_SOURCE_AMI,
        SourceRegion = "eu-west-2"
    )

    ami_id = response['ImageId']

    ami_state = ''
    while ami_state != 'available':
        ami_desc = ec2_client.describe_images(ImageIds=[ami_id])
        ami_state = ami_desc['Images'][0]['State']
        print(ami_state)
        sleep(10)

    print("AWS_AMI_ID={}".format(ami_id))

print("AWS_AMI_ID={}".format(images['Images'][0]['ImageId']))