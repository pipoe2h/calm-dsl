AWS_ACCESS_KEY = '@@{CRED_AWS.username}@@'
AWS_SECRET_KEY = '@@{CRED_AWS.secret}@@'
AWS_REGION = '@@{AWS_REGION}@@'
WEB_SERVERS = '@@{ApacheAHV.address}@@,@@{ApacheAWS.private_ip_address}@@,@@{ApacheAZ.address}@@,@@{ApacheK8sDeploymentPublished_Service.ingress}@@'
elb_target_arn = '@@{AWS_ELB_TARGET_ARN}@@'
vpc_cidr = '@@{AWS_VPC_CIDR}@@'
LATEST_WEB_SERVERS = '@@{WEB_SERVERS}@@'


def ip_to_binary(ip):
    octet_list_int = ip.split(".")
    octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
    binary = ("").join(octet_list_bin)
    return binary

def get_addr_network(address, net_size):
    #Convert ip address to 32 bit binary
    ip_bin = ip_to_binary(address)
    #Extract Network ID from 32 binary
    network = ip_bin[0:32-(32-net_size)]    
    return network

def ip_in_prefix(ip_address, prefix):
    #CIDR based separation of address and network size
    [prefix_address, net_size] = prefix.split("/")
    #Convert string to int
    net_size = int(net_size)
    #Get the network ID of both prefix and ip based net size
    prefix_network = get_addr_network(prefix_address, net_size)
    ip_network = get_addr_network(ip_address, net_size)
    return ip_network == prefix_network




from boto3 import client
from boto3 import setup_default_session

setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

elb_client = client('elbv2')

# Deregister Target Members
target_list = []
for web_server in list(set(LATEST_WEB_SERVERS.split(',')) - set(WEB_SERVERS.split(','))):
    if ip_in_prefix(web_server, vpc_cidr):
        target_list.append({'Id': web_server})
    else:
        target_list.append({'Id': web_server, 'AvailabilityZone': 'all'})

response = elb_client.deregister_targets(
    TargetGroupArn=elb_target_arn,
    Targets=target_list
)

print("WEB_SERVERS={}".format(WEB_SERVERS))