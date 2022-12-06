import datetime

import boto3, os
from dotenv import load_dotenv
import time
from botocore.exceptions import ClientError

load_dotenv()

client = boto3.client('ce', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
today = datetime.date.today()
start = today.replace(day=1).strftime('%Y-%m-%d')
end = today.strftime('%Y-%m-%d')
response = client.get_cost_and_usage(
    TimePeriod={"Start": start, "End": end},
    Granularity="MONTHLY",
    Metrics=["UnblendedCost"],
    Filter={
        'Dimensions': {
            'Key': 'AZ',
            'Values': [
                'Compute',
            ],
            'MatchOptions': [
                'EQUALS',
            ]
        }
    }
)
print(response['ResultsByTime'])
print(response['ResultsByTime'][0]["TimePeriod"]["Start"])
print(response['ResultsByTime'][0]["TimePeriod"]["End"])
print(response['ResultsByTime'][0]["Total"]["UnblendedCost"]["Amount"])
