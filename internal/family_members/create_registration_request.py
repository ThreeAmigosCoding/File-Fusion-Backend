import json
import traceback
import uuid

import boto3
from botocore.config import Config

from internal.model.my_response import my_response
from boto3.dynamodb.conditions import Attr, Key
from internal.model.multimedia_metadata import MultimediaDisplay
import os

multimedia_metadata_table_name = "family_member_invitation"
multimedia_bucket_name = os.environ['MULTIMEDIA_BUCKET']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(multimedia_metadata_table_name)
cognito_client = boto3.client("cognito-idp")


def create_registration_request(event, context):
    try:
        inviter_email = event['pathParameters']['inviterEmail']

        if not check_for_invitation(event['body']['email']):
            return my_response(400, {"message": "You are already in the system!"})

        table_item = {'email': event['body']['email'],
                      'password': event['body']['password'],
                      'name': event['body']['name'],
                      'family_name': event['body']['family_name'],
                      'address': event['body']['address'],
                      'status': "pending",
                      'id': str(uuid.uuid4()),
                      'inviter_email': inviter_email}

        table.put_item(Item=table_item)

        return my_response(200, {"message": "Registration request sent!"})
    except Exception as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})


def check_for_invitation(recipient):
    response = table.query(
        KeyConditionExpression=Key('email').eq(recipient),
        FilterExpression=Attr('status').ne('declined')
    )
    items = response['Items']
    if len(items) > 0:
        return False
    return True
