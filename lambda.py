import json
from datetime import date
import boto3

AWS_REGION = 'us-west-1'
EC2_CLIENT = boto3.client('ec2', region_name=AWS_REGION)
S3_CLIENT = boto3.client('s3', region_name=AWS_REGION)


def get_volume_info():
    unattached = []
    non_encrypted = []
    non_encrypt_overall_size = 0
    unattached_overall_size = 0
    
    response = EC2_CLIENT.describe_volumes() 
    
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        
        if volume['State'] == 'available':
            unattached.append(volume_id)
            unattached_overall_size += volume['Size']
            
        if volume['Encrypted'] is False:
            non_encrypted.append(volume_id)
            non_encrypt_overall_size += volume['Size']
    
    result = [
        { "Unattahced": {
            "NumberOfVolumes": len(unattached),
            "OverallSize": unattached_overall_size
            }
        },
        { "NonEncrypted": {
            "NumberOfVolumes": len(non_encrypted),
            "OverallSize": non_encrypt_overall_size
            }
        }
    ]
    
    return result
    
    
def get_snapshot_info():
    non_encrypted = []
    non_encrypt_overall_size = 0
    
    response = EC2_CLIENT.describe_snapshots(
        Filters=[
            {'Name': 'encrypted', 'Values': ['false']},
        ],
        OwnerIds=[
            '711133426339',    
        ],
    )
    
    for snapshot in response['Snapshots']:
        non_encrypted.append(snapshot['SnapshotId'])
        non_encrypt_overall_size += snapshot['VolumeSize']
    
    result = [
        { "NonEncrypted": {
            "NumberOfSnapshots": len(non_encrypted),
            "OverallSize": non_encrypt_overall_size
            }
        }
    ]
    
    return result
    
    
def put_metrict_to_s3():
    s3_object_name = "ebs-metrics-" + str(date.today()) + ".json"
    
    metrics = {
        "Volumes" : get_volume_info(),
        "Snapshots" : get_snapshot_info()
    }

    S3_CLIENT.put_object(
        Bucket='uc6-volume-metrics',
        Key=s3_object_name,
        Body=(bytes(json.dumps(metrics).encode('UTF-8')))
    )


def lambda_handler(event, context):
    return put_metrict_to_s3() 
