import json
import traceback
import uuid

import boto3
from botocore.config import Config

from internal.model.my_response import my_response
from boto3.dynamodb.conditions import Attr
from internal.model.multimedia_metadata import MultimediaDisplay
import os

multimedia_metadata_table_name = os.environ['MULTIMEDIA_METADATA_TABLE']
albums_table_name = os.environ['ALBUMS_TABLE']
family_member_table_name = "family_member_invitation"
share_table_name = os.environ['SHARE_TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(family_member_table_name)
share_table = dynamodb.Table(share_table_name)
albums_table = dynamodb.Table(albums_table_name)
multimedia_metadata_table = dynamodb.Table(multimedia_metadata_table_name)

cognito_client = boto3.client("cognito-idp")


def manage_registration_request(event, context):
    try:
        request_id = event['pathParameters']['requestId']
        action = event['pathParameters']['approved']

        if action == "decline":
            update_invitation_status(request_id, "declined")
            return my_response(200, "User declined successfully.")

        cognito_sign_up(request_id)
        update_invitation_status(request_id, "accepted")
        share_all_with_member(request_id)
        return my_response(200, {"message": "User registered successfully."})

    except Exception as e:
        print("message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})


def update_invitation_status(request_id, status):
    update_expression = 'SET invitation_status = :val1'
    expression_attribute_values = {':val1': status}
    table.update_item(
        Key={"id": request_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return


def cognito_sign_up(request_id):
    user_response = table.get_item(
        Key={
            'id': request_id
        }
    )
    user = user_response['Item']
    response = cognito_client.sign_up(
        ClientId='1gnmhd3blailbdicplc21la1uf',
        Username=user['email'],
        Password=user['password'],
        UserAttributes=[
            {
                'Name': 'name',
                'Value': user['name']
            },
            {
                'Name': 'family_name',
                'Value': user['family_name']
            },
            {
                'Name': 'address',
                'Value': user['address']
            },
        ]
    )


def share_all_with_member(request_id):
    user_response = table.get_item(
        Key={
            'id': request_id
        }
    )
    user = user_response['Item']

    owner = user['inviter_email']
    viewer = user['email']

    albums_response = albums_table.scan(
        FilterExpression=Attr('owner').eq(owner) & Attr('deleted').ne(True) & Attr('parent').eq("")
    )
    albums = albums_response['Items']
    for album in albums:
        share_with_user(owner, viewer, album['id'], "album")

    multimedia_metadata_response = multimedia_metadata_table.scan(
        FilterExpression=Attr('username').eq(owner) & Attr('deleted').ne(True)
    )
    multimedia_metadata = multimedia_metadata_response['Items']
    for multimedia_metadata_entry in multimedia_metadata:
        share_with_user(owner, viewer, multimedia_metadata_entry['id'], "file")


def share_with_user(owner, viewer, content_id, content_type):
    item = {
        'id': str(uuid.uuid4()),
        'owner': owner,
        'contentId': content_id,
        'contentType': content_type,
        'viewer': viewer
    }
    share_table.put_item(Item=item)
