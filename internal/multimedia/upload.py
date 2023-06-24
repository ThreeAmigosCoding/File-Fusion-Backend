import json
from io import BytesIO
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from internal.model.multimedia_metadata import MultimediaMetadata

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('multimedia_metadata')


def upload_file(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "File uploaded successfully"}),
        'headers': {
            "Access-Control-Allow-Origin": "http://localhost:4200",
            "Access-Control-Allow-Headers": "Authorization",
            "Access-Control-Allow-Credentials": True
        }
    }
