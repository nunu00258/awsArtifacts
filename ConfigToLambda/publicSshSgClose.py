import json
import boto3
 
def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    id = message['resourceId']
    status = message['newEvaluationResult']['complianceType']
    if status == 'COMPLIANT':
        return 'end'
 
    ec2 = boto3.resource('ec2')
    security_group = ec2.SecurityGroup(id)
    response = security_group.revoke_ingress(
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'ToPort': 22,
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            }
        ]
    )
    print("Security Group Changed: 0.0.0.0/0 tcp/22 delete")
    return 'end'
