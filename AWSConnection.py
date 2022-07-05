import secrets
import boto3
import pandas
import json


def readAccessKey():

    pass


def connectAWS():
    access_key, secret_key = readAccessKey()
    client = boto3.client('s3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = 'ap-south-1'
    )

    # Creating the high level object oriented interface
    resource = boto3.resource(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name='ap-south-1'
    )

    # Fetch the list of existing buckets
    response = client.list_buckets()
    bucket_list = response['Buckets']
    print(bucket_list)


connectAWS()


