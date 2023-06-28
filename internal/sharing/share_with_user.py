import os
import json
import base64
import traceback
import uuid

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from internal.model.my_response import my_response

share_table_name = os.environ['SHARE_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(share_table_name)

client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_YIWsc8z0P'


def share_with_user(event, context):
    try:
        event['body'] = base64.b64decode(event['body'])
        body = json.loads(event['body'])
        user_email = body['userEmail']
        content_id = body['contentId']
        content_type = body['contentType']
        emails = body['emails']

        for email in emails:
            try:
                client.admin_get_user(
                    UserPoolId=user_pool_id,
                    Username=email
                )
            except ClientError:
                continue

            item = {
                'id': str(uuid.uuid4()),
                'owner': user_email,
                'contentId': content_id,
                'contentType': content_type,
                'viewer': email
            }
            table.put_item(Item=item)
        return my_response(200, {"message": "Shared successfully."})

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
