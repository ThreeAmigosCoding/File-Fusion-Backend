import base64
import json
import traceback
import uuid

import boto3
from botocore.config import Config

from internal.model.my_response import my_response
from boto3.dynamodb.conditions import Attr, Key
from internal.model.multimedia_metadata import MultimediaDisplay
import os

family_member_table_name = "family_member_invitation"
multimedia_bucket_name = os.environ['MULTIMEDIA_BUCKET']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(family_member_table_name)
cognito_client = boto3.client("cognito-idp")


def create_registration_request(event, context):
    try:
        inviter_email = event['pathParameters']['inviterEmail']
        event['body'] = base64.b64decode(event['body'])
        body = json.loads(event['body'])

        if not check_for_invitation(body['email']):
            return my_response(400, {"message": "You are already in the system!"})

        table_item = {'email': body['email'],
                      'password': body['password'],
                      'name': body['name'],
                      'family_name': body['family_name'],
                      'address': body['address'],
                      'invitation_status': "pending",
                      'id': str(uuid.uuid4()),
                      'inviter_email': inviter_email}

        table.put_item(Item=table_item)

        return my_response(200, {"message": "Registration request sent!"})
    except Exception as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})


def check_for_invitation(recipient):
    response = table.scan(
        FilterExpression=Attr('email').eq(recipient) & Attr('invitation_status').ne('declined')
    )
    items = response['Items']
    if len(items) > 0:
        return False
    return True
