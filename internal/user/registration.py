import hashlib
import json

import boto3 as boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user')


def registration(event, context):
    user = json.loads(event['body'])

    # Hash the password for storage
    user['password'] = hashlib.sha256(user['password'].encode('utf-8')).hexdigest()

    # Check if the username already exists
    try:
        response = table.get_item(Key={'username': user['username']})
        if 'Item' in response:
            return {
                'statusCode': 400,
                'body': json.dumps('Username already taken!')
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

    # If username is not taken, store the user
    try:
        table.put_item(Item=user)
        return {
            'statusCode': 200,
            'body': json.dumps(user)
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }