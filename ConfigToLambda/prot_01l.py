import boto3, json
# delete defaltVPC for All regions


def get_Boto3Client(service_name, sso_user_credentials, region_name):
    client_to_return = ''
    try:
        client_to_return = boto3.client(
            service_name,
            aws_access_key_id=sso_user_credentials['AccessKeyId'],
            aws_secret_access_key=sso_user_credentials['SecretAccessKey'],
            aws_session_token=sso_user_credentials['SessionToken'],
            region_name=region_name
        )
    except Exception as e:
        print('[Exeprion ] ', e)
        client_to_return = None
    finally:
        return client_to_return

def get_AllRegions(ec2_client):
    map_to_return = []
    pre_map = map(lambda x: x['RegionName'], ec2_client.describe_regions()['Regions'])
    if pre_map is not None:
        map_to_return = pre_map
    return map_to_return

def get_DefaultVpcId(ec2_client):
    defaultVpc_map = map(lambda x: x['VpcId'],
        ec2_client.describe_vpcs(
            Filters=[{'Name': 'isDefault', 'Values': ['true', ]}, ], 
        )['Vpcs']
    )
    return defaultVpc_map

def delete_InternetGateway(ec2_client, default_vpcId):
    igwId_map = map(lambda x: x['InternetGatewayId'], 
        ec2_client.describe_internet_gateways(
            Filters=[{'Name': 'attachment.vpc-id', 'Values': [default_vpcId, ]}, ], 
        )['InternetGateways']
    )
    # DefaultVPCに関連付けられたIGWをデタッチ＆削除
    for igwId in igwId_map:
        ec2_client.detach_internet_gateway(InternetGatewayId=igwId, VpcId=default_vpcId)
        ec2_client.delete_internet_gateway(InternetGatewayId=igwId)

def delete_Subnet(ec2_client, default_vpcId):
    subnetId_map = map(lambda x: x['SubnetId'],
        ec2_client.describe_subnets(
            Filters=[{'Name': 'vpc-id', 'Values': [default_vpcId, ]}, ], 
        )['Subnets']
    )
    # DefaultVPC内のサブネットを削除
    for subnetId in subnetId_map:
        ec2_client.delete_subnet(SubnetId=subnetId)

def delete_Vpc(ec2_client, default_vpcId):
    ec2_client.delete_vpc(VpcId=default_vpcId)

def lambda_handler(event, context):
    flag_to_return = -1
    sso_user_credentials = event['SSOUserCredentials']
    
    ec2_client = get_Boto3Client('ec2', sso_user_credentials, 'ap-northeast-1')
    regions = get_AllRegions(ec2_client)
    #regions = ['ap-northeast-1']
    for region in regions:
        ec2_client = get_Boto3Client('ec2', sso_user_credentials, region)
        defaultVpcId_map = get_DefaultVpcId(ec2_client)
        for default_vpcId in defaultVpcId_map:
            delete_InternetGateway(ec2_client, default_vpcId)
            delete_Subnet(ec2_client, default_vpcId)
            delete_Vpc(ec2_client, default_vpcId)


    
    
