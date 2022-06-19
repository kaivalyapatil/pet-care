import boto3
import logging
from botocore.exceptions import ClientError
import os

def upload_file(file_data,bucket_name,object_name):
    #Upload file to S3
    try:
        # Use credentials when running from Docker
        region=os.environ["AWS_REGION"]
        access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        s3_client = boto3.client("s3", 
            region_name=region,
            aws_access_key_id=access_key_id,  
            aws_secret_access_key=secret_access_key)    
    except Exception  as ex:
        # Use default profile when running in local machine
        s3_client = boto3.client("s3")   


    try:        
        s3_client.upload_fileobj(file_data, bucket_name, object_name)
        print("File uploaded")
    except ClientError as e:
        logging.error(e)
        return False
    return True