import boto3, os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))


