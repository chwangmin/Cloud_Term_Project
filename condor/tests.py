import boto3, os
from dotenv import load_dotenv
import time
from botocore.exceptions import ClientError

load_dotenv()

ssm_client = boto3.client('ssm', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

response = ssm_client.send_command(
            InstanceIds=['i-0b3f79839ccbc2eae'],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['condor_status']}, )

time.sleep(1)

command_id = response['Command']['CommandId']
output = ssm_client.get_command_invocation(
      CommandId=command_id,
      InstanceId='i-0b3f79839ccbc2eae',
    )
print(output)