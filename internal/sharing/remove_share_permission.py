import os
import traceback
import boto3
from boto3.dynamodb.conditions import Attr
from internal.model.my_response import my_response

share_table_name = os.environ['SHARE_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(share_table_name)


def remove_share_permission(event, context):
    try:
        owner_email = event['pathParameters']['ownerEmail']
        sharing_email = event['pathParameters']['sharingEmail']
        content_id = event['pathParameters']['contentId']

        item = table.scan(
            FilterExpression=Attr('owner').eq(owner_email) & Attr('viewer').eq(sharing_email)
                             & Attr('contentId').eq(content_id)
        )
        if not item['Items']:
            return my_response(500, {"message": "No such table row."})

        row_to_remove = item['Items'][0]
        table.delete_item(
            Key={
                'id': row_to_remove['id']
            }
        )

        return my_response(200, {"message": "Sharing successfully revoked."})

    except Exception as e:
        print("error message", str(e))
        print("traceback", traceback.format_exc())
        return my_response(500, {"message": str(e), "tracebck": traceback.format_exc()})
