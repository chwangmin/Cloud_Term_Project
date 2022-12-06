import datetime

import boto3, os
from dotenv import load_dotenv
import time
from botocore.exceptions import ClientError

load_dotenv()

ses_client = boto3.client('ses', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name = "ap-northeast-2")
email = 'ckm7907@naver.com'
response = ses_client.verify_email_identity(
    EmailAddress=email
)
print(response)

CHARSET = "UTF-8"

response = ses_client.send_email(
    Destination={
        "ToAddresses": [
            "ckm7907@naver.com",
        ],
    },
    Message={
        "Body": {
            "Text": {
                "Charset": CHARSET,
                "Data": "Hello, world!",
            }
        },
        "Subject": {
            "Charset": CHARSET,
            "Data": "Amazing Email Tutorial",
        },
    },
    Source="ckm7907@naver.com",
)
