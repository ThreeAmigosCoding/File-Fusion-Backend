import base64
import json
import traceback
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from internal.model.my_response import my_response
from boto3.dynamodb.conditions import Attr, Key
from internal.model.multimedia_metadata import MultimediaDisplay

family_member_table_name = "family_member_invitation"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(family_member_table_name)


def get_members_by_status(event, context):
    try:
        inviter_email = event['pathParameters']['inviterEmail']
        invitation_status = event['pathParameters']['invitationStatus']

        response = table.scan(
            FilterExpression=Attr('inviter_email').eq(inviter_email) & Attr('invitation_status').eq(invitation_status)
        )
        items = response['Items']
        return my_response(200, items)
    except Exception as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
