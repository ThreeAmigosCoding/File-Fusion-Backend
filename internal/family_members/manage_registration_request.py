import json
import traceback

import boto3
from botocore.config import Config

from internal.model.my_response import my_response
from boto3.dynamodb.conditions import Attr
from internal.model.multimedia_metadata import MultimediaDisplay
import os

family_member_table_name = "family_member_invitation"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(family_member_table_name)
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
