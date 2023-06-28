import os
import traceback
import boto3
from boto3.dynamodb.conditions import Attr
from internal.model.my_response import my_response

share_table_name = os.environ['SHARE_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(share_table_name)


def get_shared_users(event, context):
    try:
        owner_email = event['pathParameters']['ownerEmail']
        content_id = event['pathParameters']['contentId']
        response = table.scan(
            FilterExpression=Attr('owner').eq(owner_email) & Attr('contentId').eq(content_id)
        )
        items = response['Items']
        viewers = []
        for item in items:
            viewer = item['viewer']
            viewers.append(viewer)

        return my_response(200, viewers)

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})