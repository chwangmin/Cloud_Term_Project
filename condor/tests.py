import datetime

import boto3, os
from dotenv import load_dotenv
import time
from botocore.exceptions import ClientError

load_dotenv()

ec2client = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                         region_name="ap-northeast-2")

response = ec2client.describe_instances()
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(instance)