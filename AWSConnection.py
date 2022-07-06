import secrets
import boto3
import pandas
import json

key_file = "G:/My Douments/StudyMaterials/PythonProjects/dev_user1_accessKeys.csv"

def readAccessKey():
    keys=open(key_file,'r').readlines()[1].strip()
    return keys.split(",")

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
    bucket_list = response['Buckets'][0]['Name']
    print(bucket_list)

    # Create the S3 object
    obj = client.get_object(
        Bucket=bucket_list,
        Key="SampleExpenseData.csv"
    )

    # Read data from the S3 object
    #fobj=open(obj['Body'],'r')
    #data= fobj.readlines()

    data = pandas.read_csv(obj['Body'], header=0)



    # Print the data frame
    print('Printing the data frame...')
    print(data.head())
    return data


#connectAWS()


