import json
from botocore.exceptions import ClientError
import boto3


def hello_world(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Hello world"}),
        'headers': {
            "Access-Control-Allow-Origin": "http://localhost:4200",
            "Access-Control-Allow-Headers": "Authorization",
            "Access-Control-Allow-Credentials": True
        }
    }
